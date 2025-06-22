import boto3
import hashlib
import uuid
from datetime import datetime, timedelta
import json

# Hashear contraseña
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def lambda_handler(event, context):
    try:
        # Parsear el body
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No se encontró el body en el request'})
            }

        if isinstance(event['body'], str):
            body = json.loads(event['body'])
        else:
            body = event['body']

        # Extraer campos
        user_id = body['user_id']
        password = body['password']
        hashed_password = hash_password(password)

        # Buscar usuario
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('t_users')
        response = table.get_item(Key={'user_id': user_id})

        if 'Item' not in response:
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Usuario no existe'})
            }

        hashed_password_bd = response['Item']['password']
        if hashed_password == hashed_password_bd:
            # Generar token y guardar
            token = str(uuid.uuid4())
            fecha_hora_exp = datetime.now() + timedelta(minutes=60)
            registro = {
                'token': token,
                'expires': fecha_hora_exp.strftime('%Y-%m-%d %H:%M:%S')
            }
            table = dynamodb.Table('t_tokens_acceso')
            table.put_item(Item=registro)

            return {
                'statusCode': 200,
                'body': json.dumps({'token': token})
            }

        else:
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Password incorrecto'})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error interno: {str(e)}'})
        }
