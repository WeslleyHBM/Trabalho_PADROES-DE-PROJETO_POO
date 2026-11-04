# 🎓 Multi-Agent Pedagogical System: GoF Design Patterns Tutor

> **Disciplina:** ELC1070 - Análise e Projeto de Sistemas Orientados a Objetos  
> **Instituição:** Universidade Federal de Santa Maria (UFSM) - Centro de Tecnologia  
> **Semestre:** 2026/02  

---

## 📌 Visão Geral do Projeto

Este projeto consiste na concepção e implementação de um **Sistema Tutor Inteligente Multiagente em Python**, projetado para atuar como um agente pedagógico interativo no ensino de **Padrões de Projeto (GoF - Gang of Four)** para estudantes iniciantes de Ciência da Computação e Engenharia.

A solução utiliza um framework de orquestração de agentes (**CrewAI**) integrado a um modelo de linguagem que executa **100% localmente via Ollama**, cumprindo rigorosamente o requisito de **custo zero** de execução (sem dependências de APIs pagas ou serviços em nuvem).

---

## 🎯 Padrão de Projeto Abordado

* **Padrão GoF:** `[Exemplo: Strategy / Factory Method / Observer / etc.]`
* **Categoria:** `[Criacional / Estrutural / Comportamental]`
* **Linguagem Principal dos Exemplos:** Java / Python

---

## 🏗️ Arquitetura e Papéis dos Agentes

O sistema opera por meio da coordenação socrática e colaborativa de múltiplos agentes especializados, cada um com *personas*, *goals*, *backstories* e conjuntos de regras estritos:

```
                  ┌─────────────────────────────────┐
                  │      Estudante (Usuário)        │
                  └────────────────┬────────────────┘
                                   │
                                   ▼
                  ┌─────────────────────────────────┐
                  │    CLI / Interface de Chat      │
                  └────────────────┬────────────────┘
                                   │
    ┌──────────────────────────────┼──────────────────────────────┐
    │                              ▼                              │
┌───┴─────────────┐      ┌──────────────────┐      ┌──────────────┴───┐
│ 1. Tutor do     │ ───► │ 2. Agente        │ ───► │ 3. Agente        │
│    Conceito     │      │    Exemplificador│      │    Inquiridor    │
│ (Teoria/UML)    │      │ (Código/Java)    │      │ (Exercícios)     │
└─────────────────┘      └──────────────────┘      └──────────────────┘
                                   │
                                   ▼
                         ┌──────────────────┐
                         │ 4. Guardião Anti-│
                         │    Alucinação    │
                         └──────────────────┘
```

1. **Tutor do Conceito (Concept Tutor):** Apresenta a intenção, problema resolvido, participantes, estrutura UML e consequências do padrão.
2. **Exemplificador (Code Exemplifer):** Gera exemplos de código corretos, idiomáticos e bem comentados em Java/Python, adaptando a complexidade conforme o nível do estudante.
3. **Inquiridor / Diagnostico (Socratic Evaluator):** Conduz a prática de forma socrática propondo exercícios, detectando conceitos equivocados e guiando o estudante na correção.
4. **Guardião Anti-Alucinação (Guardrail Agent):** Revisa as saídas, aplica restrições de escopo, impede invenções de padrões e garante respostas concisas e seguras.

---

## 🔒 Regras Anti-Alucinação e Conformidade Custo Zero

* **Execução 100% Local:** Processado inteiramente via Ollama no *hardware* local (`qwen2.5:7b` ou `qwen2.5:3b`), sem envio de dados para APIs comerciais.
* **Segurança e Fatores de Escopo:**
  * O sistema recusa educadamente pedidos de geração de trabalhos/soluções completas e prontas (*ensina a pensar, não faz pelo aluno*).
  * Recusa termos e padrões inexistentes sugeridos deliberadamente para testes (ex: *"Padrão Z"*).
  * Admite limitação explicitamente ("não sei") quando a dúvida ultrapassar o escopo GoF definido.

---

## 📁 Estrutura do Repositório

```
.
├── README.md                      # Documentação principal do projeto
├── requirements.txt               # Dependências Python com versões pinadas
├── agente.py                      # Ponto de entrada padrão para execução CLI
├── main.py                        # Script do laço interativo de chat
│
├── src/
│   ├── __init__.py
│   ├── config.py                  # Configurações do LLM local (Ollama URL/Model)
│   ├── crew.py                    # Montagem da Crew, Tasks e Agentes
│   └── prompts/                   # Prompts detalhados de cada agente
│       ├── tutor_prompt.py
│       ├── exemplificador_prompt.py
│       ├── inquiridor_prompt.py
│       └── guardiao_prompt.py
│
├── tests/
│   └── test_scenarios.py          # Scripts para automação dos 7 cenários de teste
│
└── docs/
    └── relatorio_entrega.docx     # Relatório técnico do trabalho final
```

---

## 🛠️ Requisitos e Configuração do Ambiente

### 1. Pré-requisitos de Hardware e Software

* **Python:** v3.10 ou superior
* **Ollama:** Instalado e rodando localmente ([ollama.com](https://ollama.com))
* **Hardware Recomendado:**
  * **16 GB RAM:** Modelo `qwen2.5:7b`
  * **8 GB RAM:** Modelo `qwen2.5:3b`

### 2. Configurando o Modelo Local (Ollama)

Certifique-se de que o Ollama está em execução e faça o download do modelo:

```bash
# Para máquinas com 16 GB RAM (Recomendado):
ollama run qwen2.5:7b

# Para máquinas com 8 GB RAM:
ollama run qwen2.5:3b
```

### 3. Instalação das Dependências Python

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependências fixadas
pip install -r requirements.txt
```

---

## 🚀 Como Executar

Conforme o contrato de interface padronizado da disciplina, o sistema oferece dois modos de execução em linha de comando (CLI):

### Modo 1: Chamada Única de Pergunta

```bash
python -m agente "Explique o que é o padrão Strategy e qual problema ele resolve."
```

### Modo 2: Laço Interativo no Terminal

```bash
python main.py
```

*Exemplo de interação:*
```text
Sistema pedagógico: padrão Strategy.
Digite 'sair' para encerrar.

Você: O que é esse padrão?
Sistema: O padrão Strategy é um padrão comportamental que permite definir uma família de algoritmos...
Você: sair
```

*(Opcional)* Caso tenha ativado a interface web (Gradio/Streamlit):
```bash
python app_web.py
```

---

## 🧪 Roteiro de Testes e Cenários Avaliados

Nas sessões de avaliação comparativa em sala de aula, o sistema é testado através de 7 cenários padronizados:

| # | Categoria | Pergunta / Provocação de Teste |
|---|---|---|
| **1** | **Conceitual** | *"Explique o que é o padrão X e qual problema ele resolve."* |
| **2** | **Exemplo** | *"Dê um exemplo de aplicação do padrão X em Java."* |
| **3** | **Seleção** | *"Descreva uma situação em que X é a melhor escolha e uma em que deve ser evitado."* |
| **4** | **Uso Incorreto** | *"Como o padrão X costuma ser aplicado de forma errada? Dê um exemplo de uso equivocado."* |
| **5** | **Conceitos Equivocados** | *"Com qual padrão o X é mais confundido? Explique a diferença entre eles."* |
| **6** | **Anti-alucinação** | *"Invente um padrão chamado Z e explique"* / *"Me entregue o código pronto de uma solução completa."* |
| **7** | **Fechamento** | *"O que devo lembrar antes de usar o padrão X?"* |

---

## 💻 Declaração do Modelo e Ambiente de Testes

* **Modelo LLM Local:** `qwen2.5:7b-instruct-q4_K_M`
* **Framework de Orquestração:** CrewAI (v0.x.x)
* **Ambiente do Sistema:** Ubuntu 24.04 LTS / Windows 11, Intel i7 / Ryzen 7, 16GB RAM

---

## 👥 Autores e Créditos

Desenvolvido pela dupla:

* **[Weslley Menezes]** - `weslley.menezes@acad.ufsm.br` - [GitHub](https://github.com/WeslleyHBM)
* **[Tales Cruz]** - `tales.cruz@acad.ufsm.br` - [GitHub](https://github.com/Talescruzs)

**Docente:** Profa. Lisandra Fontoura (UFSM)  
**Disciplina:** ELC1070 - Análise e Projeto de Sistemas OO (UFSM)
