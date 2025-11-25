import psycopg2
import pandas as pd
import json
import os

# -------------------------
# PostgreSQL connection
# -------------------------
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="people_unified",
    user="postgres",
    password="Home@2216"
)
cursor = conn.cursor()

# -------------------------
# Create output folder
# -------------------------
OUTPUT_DIR = "sample-output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------
# 1️⃣ Export 100 real rows from unified_people
# -------------------------
print("Extracting sample dataset...")

query = """
    SELECT *
    FROM unified_people
    LIMIT 100;
"""

df = pd.read_sql(query, conn)
sample_csv = os.path.join(OUTPUT_DIR, "unified-dataset-sample.csv")
df.to_csv(sample_csv, index=False)

print("✔ Saved:", sample_csv)

# -------------------------
# 2️⃣ Export Last 20 API logs (if table exists)
# -------------------------
print("Extracting sample API logs...")

try:
    query_logs = """
        SELECT *
        FROM api_logs
        ORDER BY timestamp DESC
        LIMIT 20;
    """
    cursor.execute(query_logs)
    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]
    logs_list = [dict(zip(columns, r)) for r in rows]

    sample_json = os.path.join(OUTPUT_DIR, "api-log.json")
    with open(sample_json, "w") as f:
        json.dump(logs_list, f, indent=4)

    print("✔ Saved:", sample_json)

except Exception as e:
    print("⚠ No api_logs table found. Skipping log export.")
    print(e)

cursor.close()
conn.close()
print("\n🎉 DONE — Sample outputs generated!")
