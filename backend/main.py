from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_db_connection

class IngredientRequest(BaseModel):
    text: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from backend!"}

@app.post("/scan-ingredient")

async def scan_ingredient(request: IngredientRequest):
    conn = await get_db_connection()
    try:
        query = "SELECT name, risk_level, description FROM ingredients WHERE position(lower(name) in lower($1)) > 0"
        rows = await conn.fetch(query, request.text)
        results =[]
        for row in rows:
            results.append({
                "name": row["name"],
                "risk_level": row["risk_level"],
                "description": row["description"]
            })
        return {"toxic_ingredients": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing ingredients: {str(e)}")
    finally:
        await conn.close()