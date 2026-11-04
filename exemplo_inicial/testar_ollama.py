"""Testa o acesso do CrewAI ao endpoint OpenAI-compatível do Ollama."""
from agente.llm import criar_llm


def main() -> None:
    llm = criar_llm()
    resposta = llm.call("Responda apenas: Ollama conectado ao CrewAI.")
    print(resposta)


if __name__ == "__main__":
    main()
