from fastapi import APIRouter, Depends
from auth import verify_api_key
from db import get_connection, release_connection

router = APIRouter()

# -----------------------------
# Check remaining credits
# -----------------------------
@router.get("/credits")
def get_credits(user=Depends(verify_api_key)):
    return {"user_id": user["user_id"], "credits": user["credits"]}

# -----------------------------
# Admin: Add or Set Credits
# -----------------------------
@router.post("/credits/add")
def add_credits(user_id: int, amount: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE api_users SET credits = credits + %s WHERE id = %s", (amount, user_id))
    conn.commit()

    release_connection(conn)
    return {"status": "success", "added": amount, "user_id": user_id}

@router.post("/credits/set")
def set_credits(user_id: int, amount: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE api_users SET credits = %s WHERE id = %s", (amount, user_id))
    conn.commit()

    release_connection(conn)
    return {"status": "success", "set_to": amount, "user_id": user_id}

