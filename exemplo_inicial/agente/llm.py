"""Configuração central do modelo Ollama usado por todos os agentes."""
import os

from crewai import LLM


def criar_llm() -> LLM:
    """Cria o LLM usando a API compatível com OpenAI exposta pelo Ollama.

    O nome do serviço `ollama` é resolvido pela rede interna do Docker Compose.
    custom_openai=True evita o caminho LiteLLM do prefixo `ollama/`.
    """
    modelo = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434/v1")
    timeout = int(os.getenv("OLLAMA_TIMEOUT", "600"))
    temperature = float(os.getenv("OLLAMA_TEMPERATURE", "0.5"))

    return LLM(
        model=modelo,
        custom_openai=True,
        base_url=base_url,
        api_key="ollama",  # O Ollama ignora a chave; o cliente OpenAI exige um valor.
        temperature=temperature,
        timeout=timeout,
    )
