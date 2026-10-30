import psycopg2
from psycopg2.extras import RealDictCursor


DB_SETTINGS = {
    "host": "localhost",
    "port": "5432",
    "dbname": "inventory_db",
    "user": "postgres",
    "password": "Ravi@8985",
}


def get_connection():
    return psycopg2.connect(
        host=DB_SETTINGS["host"],
        port=DB_SETTINGS["port"],
        dbname=DB_SETTINGS["dbname"],
        user=DB_SETTINGS["user"],
        password=DB_SETTINGS["password"],
        cursor_factory=RealDictCursor,
    )