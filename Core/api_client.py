import os
import requests
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
JARVIS_SECRET_KEY = os.getenv("JARVIS_SECRET_KEY", "")
HEADERS = {"X-API-Key": JARVIS_SECRET_KEY, "Content-Type": "application/json"}


def verificar_status_servidor() -> bool:
    try:
        resposta = requests.get(f"{BACKEND_URL}/health", timeout=10)
        return resposta.status_code == 200
    except requests.exceptions.RequestException:
        return False


def enviar_mensagem(texto: str) -> dict:
    try:
        resposta = requests.post(
            f"{BACKEND_URL}/chat",
            headers=HEADERS,
            json={"message": texto},
            timeout=60,
        )
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        return {"tipo": "texto", "resposta": f"Falha ao contatar o servidor: {e}"}