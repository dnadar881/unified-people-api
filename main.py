from fastapi import FastAPI
from routers import search, credits, admin, logs

app = FastAPI(title="Unified People API", version="1.0")

app.include_router(search.router)
app.include_router(credits.router)
app.include_router(admin.router)
app.include_router(logs.router)


@app.get("/")
def home():
    return {"message": "Unified People API Running!"}
