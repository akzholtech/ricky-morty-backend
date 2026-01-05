import os
import requests
from core.settings import settings


HF_API_KEY = settings.hf_token

if not HF_API_KEY:
    raise RuntimeError("HF_API_KEY is not set")

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def hf_generate(prompt: str) -> str:
    payload = {
        "inputs": f"<s>[INST] {prompt} [/INST]",
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=120)
    response.raise_for_status()

    data = response.json()

    return data[0]["generated_text"]
