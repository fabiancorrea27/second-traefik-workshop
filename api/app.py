from flask import Flask, request, jsonify
from neo4j import GraphDatabase
import os
import random

app = Flask(__name__)

# --- Configuración de Neo4j ---
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")
uri = os.getenv("NEO4J_URI")
driver = GraphDatabase.driver(uri, auth=(user, password))


# --- Función para obtener artistas y sus canciones con paginación ---
def get_artistas_paginated(tx, skip, limit):
    query = """
    MATCH (a:Artista)-[:CREO]->(c:Cancion)
    RETURN a.nombre AS artista, collect(c.nombre) AS canciones
    ORDER BY a.nombre
    SKIP $skip LIMIT $limit
    """
    result = tx.run(query, skip=skip, limit=limit)
    return [record.data() for record in result]


# --- Función para crear artista y canción ---
def create_artista_cancion(tx, artista, cancion):
    query = """
    MERGE (a:Artista {nombre: $artista})
    MERGE (c:Cancion {nombre: $cancion})
    MERGE (a)-[:CREO]->(c)
    RETURN a.nombre AS artista, c.nombre AS cancion
    """
    result = tx.run(query, artista=artista, cancion=cancion)
    return result.single().data()


# Obtener todas las canciones con paginación
def get_canciones_paginated(tx, skip, limit):
    query = """
    MATCH (c:Cancion)
    OPTIONAL MATCH (a:Artista)-[:CREO]->(c)
    RETURN c.nombre AS cancion, collect(a.nombre) AS artistas
    ORDER BY c.nombre
    SKIP $skip LIMIT $limit
    """
    result = tx.run(query, skip=skip, limit=limit)
    return [record.data() for record in result]


# Crear una canción y opcionalmente asignarla a un artista
def create_cancion(tx, nombre, artista=None):
    if artista:
        query = """
        MERGE (c:Cancion {nombre: $nombre})
        MERGE (a:Artista {nombre: $artista})
        MERGE (a)-[:CREO]->(c)
        RETURN c.nombre AS cancion, a.nombre AS artista
        """
        result = tx.run(query, nombre=nombre, artista=artista)
    else:
        query = "CREATE (c:Cancion {nombre: $nombre}) RETURN c.nombre AS cancion"
        result = tx.run(query, nombre=nombre)
    return result.single().data()


# --- Endpoint GET con paginación ---
@app.route("/artistas", methods=["GET"])
def artistas():
    page = int(request.args.get("page", 1))
    per_page = 50
    skip = (page - 1) * per_page

    with driver.session() as session:
        artistas_list = session.execute_read(get_artistas_paginated, skip, per_page)

    return jsonify({"page": page, "per_page": per_page, "results": artistas_list})


# --- Endpoint POST para insertar artista/canción ---
@app.route("/artistas", methods=["POST"])
def add_artista():
    data = request.get_json(silent=True) or {}

    # Valores random en caso de datos faltantes
    artistas_random = ["Artista Fantasma", "Los Perdidos", "Anonimus Band"]
    canciones_random = ["Canción Oculta", "Tema Secreto", "Melodía Desconocida"]

    artista = data.get("nombre") or random.choice(artistas_random)
    cancion = data.get("cancion") or random.choice(canciones_random)

    with driver.session() as session:
        nuevo = session.execute_write(create_artista_cancion, artista, cancion)

    return (
        jsonify({"message": "Artista y canción creados correctamente", "data": nuevo}),
        201,
    )


# GET /canciones?page=N
@app.route("/canciones", methods=["GET"])
def canciones():
    page = int(request.args.get("page", 1))
    per_page = 50
    skip = (page - 1) * per_page

    with driver.session() as session:
        canciones_list = session.execute_read(get_canciones_paginated, skip, per_page)

    return jsonify({"page": page, "per_page": per_page, "results": canciones_list})


# POST /canciones
@app.route("/canciones", methods=["POST"])
def add_cancion():
    data = request.get_json(silent=True) or {}

    canciones_random = ["Tema Secreto", "Melodía Desconocida", "Canción Oculta"]
    artistas_random = ["Artista Fantasma", "Los Perdidos", "Anonimus Band"]

    nombre = data.get("nombre") or random.choice(canciones_random)
    artista = data.get("artista") or random.choice(artistas_random)

    with driver.session() as session:
        nueva = session.execute_write(create_cancion, nombre, artista)

    return jsonify({"message": "Canción creada correctamente", "data": nueva}), 201


@app.route("/health")
def health():
    return "OK", 200


@app.route("/ejemplo")
def ejemplo():
    return jsonify(
        {"message": "Hola desde la API", "host": os.uname()[1]}  # Nombre del contenedor
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
