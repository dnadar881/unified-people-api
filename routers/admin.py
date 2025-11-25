from fastapi import APIRouter, HTTPException
from db import get_connection, release_connection

router = APIRouter()


@router.post("/admin/add_credits")
def add_credits(api_key: str, amount: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM api_users WHERE api_key = %s", (api_key,))
    user = cur.fetchone()

    if not user:
        release_connection(conn)
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user[0]

    cur.execute("UPDATE api_users SET credits = credits + %s WHERE id = %s",
                (amount, user_id))
    conn.commit()

    release_connection(conn)
    return {"status": "success", "added": amount}

