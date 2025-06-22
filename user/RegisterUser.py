import json

def lambda_handler(event, context):
    try:
        # Asegurarse de que 'body' exista y sea un diccionario
        if 'body' not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No se encontró el body en el request"})
            }

        # Si body viene como string (caso común en API Gateway)
        if isinstance(event['body'], str):
            body = json.loads(event['body'])
        else:
            body = event['body']

        # Validación obligatoria
        required_fields = ['email', 'username', 'password']
        for field in required_fields:
            if field not in body or not body[field]:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": f"El campo '{field}' es obligatorio"})
                }

        email = body['email']
        username = body['username']
        password = body['password']

        # Aquí va tu lógica de registro o validación
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Datos recibidos correctamente",
                "email": email,
                "username": username
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Error interno: {str(e)}"})
        }
