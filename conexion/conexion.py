import psycopg2
from flask import current_app


def get_db_connection():

    host = current_app.config["POSTGRES_HOST"]

    # PostgreSQL local no necesita SSL.
    # Neon en Render sí utiliza SSL.
    if host in ["localhost", "127.0.0.1"]:
        return psycopg2.connect(
            host=host,
            port=current_app.config["POSTGRES_PORT"],
            dbname=current_app.config["POSTGRES_DB"],
            user=current_app.config["POSTGRES_USER"],
            password=current_app.config["POSTGRES_PASSWORD"]
        )

    # Conexiones externas como Neon utilizan SSL.
    return psycopg2.connect(
        host=host,
        port=current_app.config["POSTGRES_PORT"],
        dbname=current_app.config["POSTGRES_DB"],
        user=current_app.config["POSTGRES_USER"],
        password=current_app.config["POSTGRES_PASSWORD"],
        sslmode="require"
    )