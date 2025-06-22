import json
import boto3
import hashlib
import uuid
import tempfile
import os
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

# Parámetros de configuración
BUCKET_NAME = 'utec-diagrams'

headers = {
    "Access-Control-Allow-Origin": "http://localhost:5173",
    "Access-Control-Allow-Credentials": "true"
}

def parse_json(obj, parent_key, graph):
    if isinstance(obj, dict):
        for k, v in obj.items():
            node_key = f"{parent_key}.{k}" if parent_key else k
            graph.add_edge(parent_key, node_key)
            parse_json(v, node_key, graph)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            node_key = f"{parent_key}[{i}]"
            graph.add_edge(parent_key, node_key)
            parse_json(item, node_key, graph)
    else:
        value_node = f"value: {obj}"
        graph.add_edge(parent_key, value_node)

def lambda_handler(event, context):
    print("Evento recibido:", event)

    try:
        if 'body' not in event:
            return {
                "headers": headers,
                "statusCode": 400,
                "body": json.dumps({"error": "No se encontró el body en el request"})
            }

        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        token = event['headers'].get('Authorization')  # Token en encabezado

        if not token:
            return {
                "headers": headers,
                "statusCode": 401,
                "body": json.dumps({"error": "Token requerido"})
            }

        # Validar token en DynamoDB
        dynamodb = boto3.resource('dynamodb')
        tokens_table = dynamodb.Table('t_tokens_access')
        token_resp = tokens_table.get_item(Key={'token': token})

        if 'Item' not in token_resp:
            return {
                "headers": headers,
                "statusCode": 403,
                "body": json.dumps({"error": "Token inválido"})
            }

        # Extraer JSON a graficar
        if 'json' not in body:
            return {
                "headers": headers,
                "statusCode": 400,
                "body": json.dumps({"error": "Debes enviar el campo 'json'"})
            }

        json_data = body['json']
        root = list(json_data.keys())[0]
        G = nx.DiGraph()
        G.add_node(root)
        parse_json(json_data[root], root, G)

        # Crear imagen temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
            plt.figure(figsize=(12, 10))
            pos = nx.spring_layout(G, k=0.5, iterations=50)
            nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=1800, font_size=9)
            plt.axis('off')
            plt.title("Estructura del JSON")
            plt.savefig(tmpfile.name)
            image_path = tmpfile.name

        # Subir a S3
        s3 = boto3.client('s3')
        filename = f"graphs/{str(uuid.uuid4())}.png"
        s3.upload_file(image_path, BUCKET_NAME, filename, ExtraArgs={'ACL': 'public-read'})

        # Limpiar archivo temporal
        os.remove(image_path)

        # URL pública si el bucket está configurado así
        url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"

        return {
            "headers": headers,
            "statusCode": 200,
            "body": json.dumps({"message": "Grafo generado exitosamente", "url": url})
        }

    except Exception as e:
        import traceback
        print("ERROR:", traceback.format_exc())
        return {
            "headers": headers,
            "statusCode": 500,
            "body": json.dumps({"error": f"Error interno: {str(e)}"})
        }
