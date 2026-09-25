import psycopg2
from flask import current_app

def get_db_connection():
    """Crea y retorna una conexión a la base de datos PostgreSQL."""

    return psycopg2.connect(
        host=current_app.config["POSTGRES_HOST"],
        port=current_app.config["POSTGRES_PORT"],
        dbname=current_app.config["POSTGRES_DB"],
        user=current_app.config["POSTGRES_USER"],
        password=current_app.config["POSTGRES_PASSWORD"],
        sslmode="require"
    )