import boto3
from datetime import datetime
import json

def lambda_handler(event, context):
    try:
        # Verificar y parsear el body
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No se encontró el body en el request'})
            }

        if isinstance(event['body'], str):
            body = json.loads(event['body'])
        else:
            body = event['body']

        # Extraer el token
        token = body['token']

        dynamodb = boto3.resource('dynamodb')
        tokens_table = dynamodb.Table('t_tokens_access')

        # Verificar si el token existe
        response = tokens_table.get_item(Key={'token': token})
        if 'Item' not in response:
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Token no existe'})
            }

        token_item = response['Item']
        expires = token_item['expires']
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if now > expires:
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Token expirado'})
            }

        # Obtener info del usuario
        user_id = token_item['user_id']
        users_table = dynamodb.Table('t_usuarios')  # Asegúrate que el nombre sea correcto
        user_response = users_table.get_item(Key={'user_id': user_id})

        if 'Item' not in user_response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Usuario no encontrado'})
            }

        user_info = user_response['Item']
        if 'password' in user_info:
            del user_info['password']  # No enviar la contraseña al frontend

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Token válido', 'user': user_info})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error interno: {str(e)}'})
        }
