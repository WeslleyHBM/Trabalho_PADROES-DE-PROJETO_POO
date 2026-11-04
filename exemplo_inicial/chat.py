"""Interface web Gradio para o sistema multiagente."""
import gradio as gr

from agente.sistema import responder


def conversar(pergunta: str, historico: list) -> str:
    # Cada pergunta é processada independentemente, conforme a proposta da atividade.
    return responder(pergunta)


demo = gr.ChatInterface(
    fn=conversar,
    title="Tutor de conceitos de OO",
    description=(
        "Faça perguntas sobre orientação a objetos. "
        "Cada resposta é produzida por três agentes em sequência usando "
        "um modelo local executado pelo Ollama no Docker."
    ),
    examples=[
        "O que é encapsulamento?",
        "Explique polimorfismo com um exemplo em Java.",
        "Qual é a diferença entre herança e composição?",
    ],
)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
