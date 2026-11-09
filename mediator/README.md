# Tutor pedagógico do padrão Mediator

Sistema multiagente local em Python, CrewAI e Ollama. Três agentes cooperam para
explicar Mediator, mostrar um exemplo Java, diagnosticar dúvidas e encerrar cada
turno com uma pergunta curta de aprendizagem. A CLI obrigatória permite uma
pergunta única ou uma conversa interativa com memória local à sessão.

O padrão ensinado é o **Mediator (GoF)**. O modelo padrão é **`qwen2.5:3b`**, em
execução local pelo Ollama. O sistema não contém chave de API paga nem chama um
serviço de inferência em nuvem.

## Requisitos

- Docker Desktop iniciado com backend WSL 2 no Windows, ou Docker Engine e o
  plugin Docker Compose em Linux/macOS.
- Conexão com a internet na primeira preparação para baixar as imagens Docker,
  as dependências Python e o modelo local. Depois, a inferência é local.
- Para o Qwen 2.5 3B, use como referência a recomendação do enunciado: cerca de
  8 GB de RAM. O modo padrão usa CPU e limita a inferência paralela a uma
  solicitação.

Não é necessário instalar Python, Ollama ou CrewAI no computador host.

## Preparar e executar no PowerShell

Na primeira vez, abra o terminal na pasta `mediator` e execute:

```powershell
Copy-Item .env.example .env
docker compose config
docker compose up -d
docker compose logs -f modelo-init
```

O serviço `modelo-init` espera o Ollama e baixa `qwen2.5:3b` para o volume
persistente `ollama_data` se ainda não estiver instalado. O primeiro download
pode demorar. Encerre o acompanhamento dos logs com `Ctrl+C`; isso não para os
containers.

### Uma pergunta (contrato obrigatório da disciplina)

```powershell
docker compose run --build --rm app python -m agente "Explique o que é o Mediator e qual problema ele resolve."
```

### Conversa com memória entre turnos

```powershell
docker compose run --build --rm app python -m agente
```

Digite perguntas em sequência e use `sair` para encerrar. A memória existe
durante essa sessão de terminal e inclui até três turnos anteriores. Ela não é
gravada em disco; iniciar outra execução começa uma nova conversa.

Se o projeto já foi construído, `--build` pode ser omitido:

```powershell
docker compose run --rm app python -m agente "Compare Mediator com Observer."
```

## Comandos úteis

```powershell
# Conferir serviços e modelo instalado
docker compose ps
docker compose exec ollama ollama list

# Acompanhar logs do servidor local
docker compose logs -f ollama

# Recriar a imagem Python após alterar o código
docker compose build app

# Parar containers e rede; manter o modelo baixado
docker compose down
```

Para apagar também o modelo local e liberar espaço, use `docker compose down -v`.
Isso remove o volume persistente `ollama_data`.

## Ajustes

O arquivo `.env` local é opcional e fica fora do controle de versão. O exemplo
define:

```env
OLLAMA_MODEL=qwen2.5:3b
OLLAMA_TEMPERATURE=0.2
OLLAMA_TIMEOUT=300
OLLAMA_MAX_HISTORY_TURNS=3
```

Temperatura baixa favorece consistência. Para manter respostas mais ágeis em
hardware modesto, o sistema usa três agentes em sequência, sem chamadas
paralelas, e limita o histórico enviado ao modelo. Se alterar `OLLAMA_MODEL`, o
serviço `modelo-init` fará o download do novo modelo na próxima execução.

### GPU NVIDIA (opcional)

O padrão é CPU. Para uma GPU NVIDIA já configurada no Docker Desktop/WSL 2:

```powershell
docker compose -f compose.yaml -f compose.nvidia.yaml up -d
```

Se o Docker não conseguir reservar a GPU, volte ao comando padrão `docker compose
up -d`.

## Estrutura

```text
mediator/
├── agente/
│   ├── conhecimento.py  # fatos canônicos, exemplo de estudo e sementes variadas
│   ├── llm.py           # cliente OpenAI-compatível local do Ollama
│   ├── memoria.py       # memória curta em processo
│   ├── prompts.py       # prompts completos dos três agentes
│   ├── seguranca.py     # validação e recusas determinísticas
│   ├── sistema.py       # orquestração CrewAI
│   └── __main__.py      # CLI
├── docs/
│   ├── caderno_evidencias.md
│   ├── justificativa_design.md
│   ├── mini_relatorio_processo.md
│   ├── prompts_agentes.md
│   └── roteiro_validacao.md
├── scripts/ensure_model.py
├── compose.yaml
├── Dockerfile
└── requirements.txt
```

## Documentação do trabalho

- [Prompts completos e coordenação](docs/prompts_agentes.md)
- [Justificativa de design](docs/justificativa_design.md)
- [Mini-relatório do processo - modelo a completar pela dupla](docs/mini_relatorio_processo.md)
- [Caderno de evidências - registros reais das sessões](docs/caderno_evidencias.md)
- [Roteiro de validação](docs/roteiro_validacao.md)
- [Exemplo Java completo](docs/exemplo_java_mediator.md)

O mini-relatório e o caderno são modelos, não registros inventados. Antes da
entrega, a dupla deve registrar sua configuração real, as iterações e testes que
executou, e as respostas que coletou ao avaliar sistemas de outras duplas.

## Limites conhecidos

- As recusas para padrão inventado e pedido de solução completa são feitas por
  regras determinísticas simples. Perguntas em linguagem ambígua ainda dependem
  da interpretação do modelo.
- A revisão por agente reduz contradições, mas não prova a correção de toda saída.
  O exemplo Java de referência e os fatos-base devem ser confrontados pela dupla
  com o material da disciplina.
- A memória é transitória e não sincroniza sessões diferentes.
- A inferência local dispensa custo por chamada, mas usa CPU/RAM e pode ser lenta
  dependendo do hardware.
