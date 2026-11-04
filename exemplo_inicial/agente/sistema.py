from crewai import Agent, Crew, Process, Task

from .llm import criar_llm


def montar_crew() -> Crew:
    """Monta a equipe de três agentes que trabalham em sequência."""
    llm = criar_llm()

    tutor = Agent(
        role="Tutor de Conceitos de Orientação a Objetos",
        goal=(
            "Ensinar os conceitos fundamentais de OO: encapsulamento, abstração, "
            "herança, polimorfismo, composição e relacionamentos entre classes; "
            "explicar o que cada conceito significa, o problema que resolve e "
            "como reconhecê-lo no código."
        ),
        backstory=(
            "Você é um professor de programação orientada a objetos, paciente "
            "e didático, especialista em fundamentos de orientação a objetos."
        ),
        llm=llm,
        verbose=True,
    )

    exemplificador = Agent(
        role="Gerador de Exemplos",
        goal=(
            "Criar exemplos em Java corretos e didáticos do conceito de "
            "orientação a objetos discutido."
        ),
        backstory=(
            "Você é um programador sênior em Java, especialista em modelagem "
            "de classes e em explicar conceitos com código simples."
        ),
        llm=llm,
        verbose=True,
    )

    avaliador = Agent(
        role="Avaliador Crítico",
        goal="Revisar se a resposta está correta e não inventa fatos.",
        backstory=(
            "Você é um revisor rigoroso: não aceita explicações incorretas "
            "nem conceitos inventados. Corrige imprecisões e aponta incertezas."
        ),
        llm=llm,
        verbose=True,
    )

    tarefa_tutor = Task(
        description=(
            "Responda à pergunta do estudante sobre conceitos de orientação "
            "a objetos: {pergunta}"
        ),
        expected_output="Explicação clara e correta em português.",
        agent=tutor,
    )

    tarefa_exemplo = Task(
        description=(
            "Complemente a explicação anterior com um exemplo em Java correto, "
            "curto e didático do conceito discutido."
        ),
        expected_output="Código Java curto, funcional e explicado.",
        agent=exemplificador,
    )

    tarefa_avaliacao = Task(
        description=(
            "Revise a explicação e o exemplo produzidos nas tarefas anteriores. "
            "Corrija erros conceituais ou de código. Não invente informações; "
            "quando houver incerteza, deixe-a explícita."
        ),
        expected_output="Resposta final revisada, clara e sem erros conhecidos.",
        agent=avaliador,
    )

    return Crew(
        agents=[tutor, exemplificador, avaliador],
        tasks=[tarefa_tutor, tarefa_exemplo, tarefa_avaliacao],
        process=Process.sequential,
        verbose=True,
    )


def responder(pergunta: str) -> str:
    """Executa a equipe e retorna a resposta final."""
    pergunta = pergunta.strip()
    if not pergunta:
        raise ValueError("A pergunta não pode estar vazia.")

    resultado = montar_crew().kickoff(inputs={"pergunta": pergunta})
    return resultado.raw
