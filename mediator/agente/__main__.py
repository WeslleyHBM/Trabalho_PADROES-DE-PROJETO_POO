import sys

from .seguranca import EntradaInvalida
from .sistema import SistemaMediator


def main() -> None:
    sistema = SistemaMediator()
    argumentos = " ".join(sys.argv[1:]).strip()

    if len(sys.argv) > 1:
        print("Modo de pergunta única, o agente vai responder e fechar a sessão.\n")
        try:
            print(sistema.responder(argumentos))
        except EntradaInvalida as erro:
            print(f"Entrada inválida: {erro}", file=sys.stderr)
            raise SystemExit(2) from erro
        except RuntimeError as erro:
            print(f"Erro: {erro}", file=sys.stderr)
            raise SystemExit(1) from erro
        return

    print("Tutor pedagógico do padrão Mediator (Qwen local)")
    print("Digite sua pergunta. Use 'sair' para encerrar.\n")
    while True:
        try:
            pergunta = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSessão encerrada.")
            return

        if pergunta.lower() in {"sair", "exit", "quit"}:
            print("Sessão encerrada.")
            return
        if not pergunta:
            print("Tutor: Digite uma pergunta antes de enviar.\n")
            continue

        try:
            print(f"\nTutor: {sistema.responder(pergunta)}\n")
        except EntradaInvalida as erro:
            print(f"Tutor: {erro}\n")
        except RuntimeError as erro:
            print(f"Tutor: {erro}\n")


if __name__ == "__main__":
    main()
