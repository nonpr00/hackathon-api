import json
import boto3
import hashlib

headers = {
    "Access-Control-Allow-Origin": "http://localhost:5173",
    "Access-Control-Allow-Credentials": "true"
}

# Hashear contraseña
def hash_password(password):
    # Retorna la contraseña hasheada
    return hashlib.sha256(password.encode()).hexdigest()

def lambda_handler(event, context):
    try:
        # Verificar que el body esté presente
        if 'body' not in event:
            return {
                "headers": headers,
                "statusCode": 400,
                "body": json.dumps({"error": "No se encontró el body en el request"})
            }

        # Parsear el body si viene como string
        if isinstance(event['body'], str):
            body = json.loads(event['body'])
        else:
            body = event['body']

        # Validar campos obligatorios
        required_fields = ['user_id', 'email', 'username', 'password']
        for field in required_fields:
            if field not in body or not body[field]:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": f"El campo '{field}' es obligatorio"})
                }

        # Extraer campos
        user_id = body['user_id']
        email = body['email']
        username = body['username']
        password = body['password']

        # Hashear la contraseña antes de guardar
        hashed_password = hash_password(password)

        # Guardar en DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('t_users')

        table.put_item(
            Item={
                'user_id': user_id,
                'email': email,
                'username': username,
                'password': hashed_password
            }
        )

        return {
            "headers": headers,
            "statusCode": 200,
            "body": json.dumps({
                "message": "Usuario registrado exitosamente",
                "user_id": user_id,
                "email": email,
                "username": username
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": f"Error interno: {str(e)}"})
        }
