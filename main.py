from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx, os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client_ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://rickandmortyapi.com/api"


@app.get("/api/characters")
async def get_characters(page: int = 1, name: str = ""):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/character", params={"page": page, "name": name})
        return res.json()


@app.get("/api/characters/{char_id}")
async def get_character(char_id: int):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/character/{char_id}")
        return res.json()


@app.get("/api/ai/character-description/{char_id}")
async def ai_description(char_id: int):
    async with httpx.AsyncClient() as client:
        char = await client.get(f"{BASE_URL}/character/{char_id}")
        char = char.json()

    prompt = f"Write a cinematic backstory for Rick and Morty character {char['name']}"

    response = client_ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"story": response.choices[0].message.content}
