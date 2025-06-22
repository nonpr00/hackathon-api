import boto3
from datetime import datetime
import json

def lambda_handler(event, context):
    token = event['token']

    dynamodb = boto3.resource('dynamodb')
    tokens_table = dynamodb.Table('t_tokens_acceso')

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
    users_table = dynamodb.Table('t_usuarios')
    user_response = users_table.get_item(Key={'user_id': user_id})

    if 'Item' not in user_response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Usuario no encontrado'})
        }

    user_info = user_response['Item']
    del user_info['password']  # No enviar password al frontend

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Token válido', 'user': user_info})
    }
