import os

from crewai import LLM


def criar_llm() -> LLM:
    modelo = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434/v1")
    timeout = int(os.getenv("OLLAMA_TIMEOUT", "300"))
    temperatura = float(os.getenv("OLLAMA_TEMPERATURE", "0.2"))

    return LLM(
        model=modelo,
        custom_openai=True,
        base_url=base_url,
        api_key="ollama",  # Valor local fictício exigido pelo cliente compatível.
        temperature=temperatura,
        timeout=timeout,
    )
