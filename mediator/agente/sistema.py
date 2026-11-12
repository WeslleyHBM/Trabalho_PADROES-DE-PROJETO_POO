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
            "Ensine o conceito do padrão Mediator para responder à dúvida atual do estudante.\n\n"
            "Use os Fatos confiáveis abaixo para explicar o problema que ele resolve, "
            "a intenção e como a coordenação funciona. Seja claro, direto e didático.\n\n"
            "Histórico da conversa:\n{memoria}\n\n"
            "Mensagem atual:\n{pergunta}\n\n"
            "Fatos confiáveis:\n{referencia}"
        ),
        expected_output="Explicação conceitual clara sobre o padrão Mediator.",
        agent=tutor,
    )

    tarefa_exemplo = Task(
        description=(
            "Você recebe a explicação do Tutor no contexto, mas sua REGRA DE DECISÃO ABSOLUTA "
            "baseia-se APENAS na Mensagem atual do usuário.\n\n"
            "Mensagem atual: '{pergunta}'\n\n"
            "-> Se o usuário NÃO pedir código, exemplo ou Java nesta mensagem específica: "
            "Sua saída deve ser EXATAMENTE E APENAS a frase: 'Posso montar um exemplo Java se você quiser.' "
            "NÃO escreva nenhuma outra palavra, não explique, não gere código.\n\n"
            "-> Se o usuário PEDIR explicitamente: Gere o código Java curto usando uma das sementes, "
            "sem repetir a memória.\n\n"
            "Sementes: {exemplos_didaticos}\n"
            "Memória: {memoria}"
        ),
        expected_output="EXATAMENTE a frase de oferta OU um código Java (se explicitamente solicitado).",
        agent=exemplificador,
        context=[tarefa_conceito],  # Mantido exatamente como você projetou!
    )

    tarefa_final = Task(
        description=(
            "Você é o revisor final. Escreva a resposta ao estudante combinando o trabalho "
            "do Tutor e do Exemplificador, usando no máximo 120 palavras.\n\n"
            "SIGA ESTA ORDEM OBRIGATÓRIA NA RESPOSTA:\n"
            "1. Explicação: Apresente o conceito revisado, corrigindo erros com os Fatos confiáveis.\n"
            "2. Código ou Oferta: Se o Exemplificador gerou código, mostre-o. Se ele apenas "
            "ofertou o exemplo ('Posso montar um exemplo...'), inclua essa frase aqui.\n"
            "3. Pergunta Socrática: A ÚLTIMA frase do seu texto DEVE SEMPRE ser uma pergunta "
            "curta para testar o que o aluno acabou de ler. Nunca termine a mensagem com a "
            "oferta de código; a pergunta socrática é obrigatoriamente o encerramento.\n\n"
            "Histórico da conversa:\n{memoria}\n\n"
            "Pergunta atual:\n{pergunta}\n\n"
            "Fatos confiáveis:\n{referencia}"
        ),
        expected_output="Resposta final de até 120 palavras, terminando obrigatoriamente com a pergunta socrática.",
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
