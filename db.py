import psycopg2
from psycopg2.pool import SimpleConnectionPool

# -----------------------------
# PostgreSQL SETTINGS
# -----------------------------
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "people_unified"
DB_USER = "postgres"
DB_PASS = "Home@2216"

# -----------------------------
# CONNECTION POOL (recommended)
# -----------------------------
try:
    pool = SimpleConnectionPool(
        1,                     # min connections
        20,                    # max connections
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )
    print("✔ PostgreSQL connection pool created")
except Exception as e:
    print("❌ Error: could not create connection pool:")
    print(e)
    pool = None


# -----------------------------
# FUNCTIONS FOR ROUTERS
# -----------------------------
def get_connection():
    """Get a PostgreSQL connection from pool."""
    if not pool:
        raise Exception("❌ PostgreSQL pool not initialized")

    return pool.getconn()


def release_connection(conn):
    """Release a PostgreSQL connection back to the pool."""
    if pool and conn:
        pool.putconn(conn)
