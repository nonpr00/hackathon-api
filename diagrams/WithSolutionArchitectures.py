'''
import uuid
import json
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.onprem.database import MySQL
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from IPython.display import Image, display

# 🎯 Código fuente desde el frontend (con clusters y tipos)
codigo_fuente = json.dumps({
    "title": "Arquitectura web",
    "clusters": {
        "Frontend": {
            "User1": "User",
            "User2": "User"
        },
        "Backend": {
            "AppServer": "Server",
            "WebServer": "Nginx"
        },
        "BaseDatos": {
            "DB": "MySQL"
        }
    },
    "edges": [
        ["User1", "WebServer"],
        ["User2", "WebServer"],
        ["WebServer", "AppServer"],
        ["AppServer", "DB"]
    ]
})

# 🧠 Diccionario de clases disponibles
NODE_TYPES = {
    "User": User,
    "Server": Server,
    "Nginx": Nginx,
    "MySQL": MySQL,
    "RDS": RDS,
    "EC2": EC2
}

def generar_diagrama_completo(codigo_json):
    try:
        datos = json.loads(codigo_json)
        titulo = datos.get("title", "Diagrama generado")
        clusters = datos.get("clusters", {})
        edges = datos.get("edges", [])

        nombre_archivo = str(uuid.uuid4())
        nodos = {}

        with Diagram(titulo, filename=nombre_archivo, outformat="png"):
            for nombre_cluster, elementos in clusters.items():
                with Cluster(nombre_cluster):
                    for nombre_nodo, tipo in elementos.items():
                        clase = NODE_TYPES.get(tipo, Server)  # por defecto Server
                        nodos[nombre_nodo] = clase(nombre_nodo)

            for origen, destino in edges:
                nodos[origen] >> nodos[destino]

        display(Image(filename=f"{nombre_archivo}.png"))

    except Exception as e:
        print("❌ Error:", e)

# 🧪 Prueba
generar_diagrama_completo(codigo_fuente)

'''