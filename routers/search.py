from fastapi import APIRouter, Query, HTTPException, Request, Response
from db import get_connection, release_connection
from auth import verify_api_key, check_rate_limit
import time
import csv
import io

router = APIRouter()

@router.get("/search")
def search_people(
    request: Request,
    q: str = None,
    first_name: str = None,
    last_name: str = None,
    email: str = None,
    company: str = None,
    country: str = None,
    limit: int = 50,
    offset: int = 0,
    format: str = "json",
    x_api_key: str = None
):
    start = time.time()

    # --- AUTH + CREDIT CHECK ---
    auth = verify_api_key(x_api_key)
    user_id = auth["user_id"]

    check_rate_limit(user_id)

    if auth["credits"] <= 0:
        raise HTTPException(402, detail="Insufficient Credits")

    conn = get_connection()
    cur = conn.cursor()

    # --- Build dynamic SQL ---
    conditions = []
    params = []

    if q:
        conditions.append("(full_name ILIKE %s OR email ILIKE %s OR company_name ILIKE %s)")
        params += [f"%{q}%", f"%{q}%", f"%{q}%"]

    if first_name:
        conditions.append("first_name ILIKE %s")
        params.append(f"%{first_name}%")

    if last_name:
        conditions.append("last_name ILIKE %s")
        params.append(f"%{last_name}%")

    if email:
        conditions.append("email ILIKE %s")
        params.append(f"%{email}%")

    if company:
        conditions.append("company_name ILIKE %s")
        params.append(f"%{company}%")

    if country:
        conditions.append("company_country ILIKE %s")
        params.append(f"%{country}%")

    where = " AND ".join(conditions) if conditions else "TRUE"

    # --- Count total ---
    cur.execute(f"SELECT COUNT(*) FROM unified_people WHERE {where}", params)
    total_records = cur.fetchone()[0]

    # --- Fetch paginated data ---
    query = f"""
        SELECT *
        FROM unified_people
        WHERE {where}
        ORDER BY last_updated DESC
        LIMIT %s OFFSET %s
    """

    final_params = params + [limit, offset]
    cur.execute(query, final_params)
    rows = cur.fetchall()
    
    duration = round((time.time() - start) * 1000, 2)

    # --- Deduct 1 credit ---
    cur.execute("UPDATE api_users SET credits = credits - 1 WHERE id = %s", (user_id,))
    conn.commit()

    # --- Log request ---
    cur.execute("""
        INSERT INTO api_logs (user_id, endpoint, query, credits_used, duration_ms)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, "/search", str(final_params), 1, duration))
    
    conn.commit()
    release_connection(conn)

    # --- CSV EXPORT ---
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([desc[0] for desc in cur.description])
        writer.writerows(rows)
        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=results.csv"}
        )

    # --- JSON response ---
    return {
        "items": rows,
        "total_records": total_records,
        "returned": len(rows),
        "limit": limit,
        "offset": offset,
        "credits_used": 1,
        "response_time_ms": duration
    }
