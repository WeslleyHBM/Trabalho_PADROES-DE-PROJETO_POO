"""Aguarda o Ollama e baixa o modelo configurado quando necessário."""

import json
import os
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434").rstrip("/")
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")


def get_json(url: str, timeout: int = 10) -> dict:
    with urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def wait_for_ollama() -> None:
    print(f"Aguardando Ollama em {OLLAMA_URL}...", flush=True)
    erro_recente = None
    for tentativa in range(1, 61):
        try:
            get_json(f"{OLLAMA_URL}/api/tags")
            print("Ollama está respondendo.", flush=True)
            return
        except (URLError, TimeoutError, OSError) as erro:
            erro_recente = erro
            print(f"Tentativa {tentativa}/60: Ollama ainda não está pronto.", flush=True)
            time.sleep(5)
    raise RuntimeError(f"Ollama não respondeu após 5 minutos: {erro_recente}")


def model_is_installed() -> bool:
    dados = get_json(f"{OLLAMA_URL}/api/tags")
    return any(
        item.get("name") == MODEL or item.get("model") == MODEL
        for item in dados.get("models", [])
    )


def pull_model() -> None:
    print(f"Baixando modelo {MODEL}...", flush=True)
    payload = json.dumps({"model": MODEL, "stream": True}).encode("utf-8")
    request = Request(
        f"{OLLAMA_URL}/api/pull",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=3600) as response:
            for linha in response:
                if not linha.strip():
                    continue
                item = json.loads(linha.decode("utf-8"))
                if item.get("error"):
                    raise RuntimeError(item["error"])
                if item.get("status"):
                    print(item["status"], flush=True)
    except HTTPError as erro:
        detalhe = erro.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Falha HTTP ao baixar o modelo: {detalhe}") from erro
    print(f"Modelo {MODEL} pronto.", flush=True)


def main() -> None:
    wait_for_ollama()
    if model_is_installed():
        print(f"Modelo {MODEL} já está instalado.", flush=True)
        return
    pull_model()


if __name__ == "__main__":
    try:
        main()
    except Exception as erro:
        print(f"Erro ao preparar o modelo: {erro}", file=sys.stderr, flush=True)
        raise SystemExit(1)
