import psycopg2
from psycopg2.pool import SimpleConnectionPool

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "people_unified"
DB_USER = "postgres"
DB_PASS = "Home@2216"

try:
    pool = SimpleConnectionPool(
        1,
        20,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )
    print("✔ PostgreSQL connection pool created")
except Exception as e:
    print("❌ Failed to create connection pool:", e)
    pool = None


def get_connection():
    if not pool:
        raise Exception("❌ PostgreSQL pool not initialized")
    return pool.getconn()


def release_connection(conn):
    if pool and conn:
        pool.putconn(conn)
