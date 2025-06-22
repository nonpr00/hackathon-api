import boto3
import hashlib
import uuid
from datetime import datetime, timedelta
import json

headers = {
    "Access-Control-Allow-Origin": "http://localhost:5173",
    "Access-Control-Allow-Credentials": "true"
}

# Hashear contraseña
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def lambda_handler(event, context):
    try:
        # Parsear body
        if 'body' not in event:
            return {
                'statusCode': 400,
                "headers": headers,
                'body': json.dumps({'error': 'No se encontró el body en el request'})
            }

        if isinstance(event['body'], str):
            body = json.loads(event['body'])
        else:
            body = event['body']

        # Validar campos
        if 'email' not in body or 'password' not in body:
            return {
                'statusCode': 400,
                "headers": headers,
                'body': json.dumps({'error': 'Faltan campos obligatorios: email o password'})
            }

        email = body['email']
        password = body['password']
        hashed_password = hash_password(password)

        # Buscar por email (scan)
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('t_users')

        response = table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('email').eq(email)
        )

        if not response['Items']:
            return {
                'statusCode': 403,
                "headers": headers,
                'body': json.dumps({'error': 'Usuario no existe'})
            }

        user = response['Items'][0]

        if hashed_password == user['password']:
            token = str(uuid.uuid4())
            fecha_hora_exp = datetime.now() + timedelta(minutes=60)
            registro = {
                'token': token,
                'expires': fecha_hora_exp.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id': user['user_id']
            }

            tokens_table = dynamodb.Table('t_tokens_acceso')
            tokens_table.put_item(Item=registro)

            return {
                'statusCode': 200,
                "headers": headers,
                'body': json.dumps({'token': token})
            }

        else:
            return {
                'statusCode': 403,
                "headers": headers,
                'body': json.dumps({'error': 'Password incorrecto'})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            "headers": headers,
            'body': json.dumps({'error': f'Error interno: {str(e)}'})
        }
