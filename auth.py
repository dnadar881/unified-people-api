from fastapi import Header, HTTPException
from db import get_connection, release_connection

# -----------------------------
# Verify API Key
# -----------------------------
def verify_api_key(x_api_key: str = Header(None)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing API Key")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, credits FROM api_users WHERE api_key = %s", (x_api_key,))
    row = cur.fetchone()

    release_connection(conn)

    if not row:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    user_id, credits = row
    return {"user_id": user_id, "credits": credits}


# -----------------------------
# Rate Limit Check
# -----------------------------
def check_rate_limit(user_id: int):
    """Limit: 60 requests per minute per user"""

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM api_logs
        WHERE user_id = %s
        AND timestamp > NOW() - INTERVAL '1 minute'
    """, (user_id,))

    count = cur.fetchone()[0]
    release_connection(conn)

    if count >= 60:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded (max 60 requests/min)"
        )


# -----------------------------
# Credit Check
# -----------------------------
def check_credits(credits: int):
    if credits <= 0:
        raise HTTPException(
            status_code=402,
            detail="Insufficient Credits"
        )
