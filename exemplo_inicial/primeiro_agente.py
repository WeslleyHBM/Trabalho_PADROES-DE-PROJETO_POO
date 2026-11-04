"""Versão inicial com apenas um agente tutor de princípios SOLID."""
import sys

from crewai import Agent, Crew, Process, Task

from agente.llm import criar_llm


def main() -> None:
    llm = criar_llm()

    tutor = Agent(
        role="Tutor de Princípios SOLID",
        goal=(
            "Ensinar os 5 princípios SOLID: o que cada um significa, "
            "qual problema resolve e como reconhecê-lo no código."
        ),
        backstory=(
            "Você é um professor de programação orientada a objetos, paciente "
            "e didático, especialista em princípios de design."
        ),
        llm=llm,
    )

    tarefa = Task(
        description=(
            "Responda à pergunta do estudante sobre os princípios SOLID: {pergunta}"
        ),
        expected_output=(
            "Explicação em português, com exemplo em Java, em até 200 palavras."
        ),
        agent=tutor,
    )

    crew = Crew(
        agents=[tutor],
        tasks=[tarefa],
        process=Process.sequential,
        verbose=True,
    )

    pergunta = " ".join(sys.argv[1:]).strip()
    if not pergunta:
        pergunta = "O que é o princípio da Responsabilidade Única?"

    resultado = crew.kickoff(inputs={"pergunta": pergunta})
    print(resultado.raw)


if __name__ == "__main__":
    main()
