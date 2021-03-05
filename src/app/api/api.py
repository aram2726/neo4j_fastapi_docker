from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
async def home():
    return JSONResponse(
        {"message": "Hello from neo4j, spark and fastapi."}
    )
