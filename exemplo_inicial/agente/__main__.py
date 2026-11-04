import sys

from .sistema import responder


def main() -> None:
    pergunta = " ".join(sys.argv[1:]).strip()
    if not pergunta:
        print('Uso: python -m agente "sua pergunta"')
        raise SystemExit(1)

    try:
        print(responder(pergunta))
    except Exception as erro:
        print(f"Erro ao executar o sistema multiagente: {erro}")
        raise SystemExit(1) from erro


if __name__ == "__main__":
    main()
