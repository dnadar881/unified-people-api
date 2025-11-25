from fastapi import APIRouter
from db import get_connection, release_connection

router = APIRouter()

@router.get("/logs")
def get_logs():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM api_logs ORDER BY timestamp DESC LIMIT 200")
    rows = cur.fetchall()
    release_connection(conn)
    return rows

