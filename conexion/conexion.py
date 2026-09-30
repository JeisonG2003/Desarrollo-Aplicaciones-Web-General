import psycopg
from psycopg.rows import dict_row
from flask import current_app

def get_db_connection():
    host = current_app.config["POSTGRES_HOST"]

    # Conexión local sin SSL
    if host in ["localhost", "127.0.0.1"]:
        return psycopg.connect(
            host=host,
            port=current_app.config["POSTGRES_PORT"],
            dbname=current_app.config["POSTGRES_DB"],
            user=current_app.config["POSTGRES_USER"],
            password=current_app.config["POSTGRES_PASSWORD"],
            row_factory=dict_row
        )

    # Conexiones externas (como Neon) con SSL
    return psycopg.connect(
        host=host,
        port=current_app.config["POSTGRES_PORT"],
        dbname=current_app.config["POSTGRES_DB"],
        user=current_app.config["POSTGRES_USER"],
        password=current_app.config["POSTGRES_PASSWORD"],  # <-- Revisa que tenga esta coma aquí
        sslmode="require",
        row_factory=dict_row
    )