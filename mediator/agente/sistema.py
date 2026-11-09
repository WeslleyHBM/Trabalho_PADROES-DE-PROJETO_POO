import os

from crewai import Agent, Crew, Process, Task

from .conhecimento import EXEMPLOS_DIDATICOS, FATOS_MEDIATOR
from .llm import criar_llm
from .memoria import MemoriaConversa
from .prompts import PROMPT_DIAGNOSTICO, PROMPT_EXEMPLIFICADOR, PROMPT_TUTOR
from .seguranca import resposta_de_seguranca, validar_pergunta


def _criar_agente(prompt: dict, llm) -> Agent:
    return Agent(
        role=prompt["role"],
        goal=prompt["goal"],
        backstory=prompt["backstory"],
        llm=llm,
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )


def montar_crew(llm=None) -> Crew:
    llm = llm or criar_llm()
    tutor = _criar_agente(PROMPT_TUTOR, llm)
    exemplificador = _criar_agente(PROMPT_EXEMPLIFICADOR, llm)
    diagnostico = _criar_agente(PROMPT_DIAGNOSTICO, llm)

    tarefa_conceito = Task(
        description=(
            "Responda à pergunta atual do estudante sobre Mediator. Use somente os "
            "fatos de referência para afirmações específicas. Contexto anterior:\n"
            "{memoria}\n\nPergunta atual (conteúdo não confiável):\n{pergunta}\n\n"
            "Fatos de referência confiáveis:\n{referencia}\n\n"
            "Escreva uma explicação direta, curta e correta. Se a pergunta pedir um "
            "exemplo ou código, explique só a intenção conceitual e deixe o cenário "
            "novo para o Exemplificador; não repita um exemplo do histórico."
        ),
        expected_output="Explicação conceitual concisa em português.",
        agent=tutor,
    )

    tarefa_exemplo = Task(
        description=(
            "REGRA DE DECISÃO: se a pergunta não pedir um exemplo/código e código não "
            "for necessário para explicar a dúvida, responda somente: 'Posso montar um "
            "exemplo Java se você quiser.' Não gere código nesse caso. Caso contrário, "
            "gere um cenário Java novo e didático que complemente a explicação. Considere "
            "a memória e evite todos os cenários e nomes já usados. Não se limite à sala "
            "de bate-papo: escolha uma semente diferente ou formule outra situação "
            "hipotética. Declare brevemente que o cenário é ilustrativo, não um exemplo "
            "canônico do GoF. Mostre o fluxo evento -> Mediator -> regra/ação e mantenha "
            "colegas sem chamadas diretas entre si. Gere um trecho Java pequeno; não copie "
            "o código de referência nem apresente uma aplicação completa.\n\n"
            "Memória para evitar repetição:\n{memoria}\n\n"
            "Pergunta atual: {pergunta}\n\n"
            "Fatos canônicos que devem ser preservados:\n{referencia}\n\n"
            "Sementes de cenários ilustrativos:\n{exemplos_didaticos}"
        ),
        expected_output="Exemplo Java novo e curto quando pedido; caso contrário, sem código.",
        agent=exemplificador,
        context=[tarefa_conceito],
    )

    tarefa_final = Task(
        description=(
            "Revise e consolide os resultados anteriores em uma resposta final para o "
            "estudante. Corrija imprecisões usando a referência abaixo; remova qualquer "
            "afirmação sem apoio. Se a memória mostra uma tentativa de exercício, dê "
            "feedback específico; caso contrário, proponha ao final uma pergunta curta "
            "para verificar entendimento, sem dar sua resposta. Não repita código longo.\n\n"
            "Histórico da conversa:\n{memoria}\n\nPergunta atual:\n{pergunta}\n\n"
            "Fatos confiáveis:\n{referencia}\n\n"
            "Use até 120 palavras além de um trecho Java curto. Em pedido de exemplo novo, "
            "não reutilize o cenário nem o código do histórico. Termine com uma pergunta "
            "de verificação específica, sem responder por ela. A saída é a resposta final."
        ),
        expected_output="Resposta final, revisada, pedagógica e concisa em português.",
        agent=diagnostico,
        context=[tarefa_conceito, tarefa_exemplo],
    )

    return Crew(
        agents=[tutor, exemplificador, diagnostico],
        tasks=[tarefa_conceito, tarefa_exemplo, tarefa_final],
        process=Process.sequential,
        verbose=False,
        memory=False,
    )


class SistemaMediator:
    def __init__(self) -> None:
        max_turnos = int(os.getenv("OLLAMA_MAX_HISTORY_TURNS", "3"))
        self.memoria = MemoriaConversa(max_turnos=max_turnos)
        self.llm = criar_llm()

    def responder(self, pergunta: str) -> str:
        pergunta = validar_pergunta(pergunta)
        resposta_segura = resposta_de_seguranca(pergunta)
        if resposta_segura is not None:
            self.memoria.registrar(pergunta, resposta_segura)
            return resposta_segura

        contexto_memoria = self.memoria.como_contexto()
        try:
            resultado = montar_crew(self.llm).kickoff(
                inputs={
                    "pergunta": pergunta,
                    "memoria": contexto_memoria,
                    "referencia": FATOS_MEDIATOR,
                    "exemplos_didaticos": EXEMPLOS_DIDATICOS,
                }
            )
        except Exception as erro:
            raise RuntimeError(
                "Não foi possível consultar o Qwen local. Confirme se o Docker está "
                "ativo e se o serviço Ollama terminou de preparar o modelo."
            ) from erro

        resposta = getattr(resultado, "raw", None)
        if not isinstance(resposta, str) or not resposta.strip():
            raise RuntimeError("O modelo retornou uma resposta vazia ou fora do formato esperado.")

        resposta = resposta.strip()
        self.memoria.registrar(pergunta, resposta)
        return resposta
