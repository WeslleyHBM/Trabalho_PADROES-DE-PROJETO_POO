# Sistema multiagente 100% em containers Docker

Projeto com dois serviços principais:

- `ollama`: servidor local de modelos de linguagem. Os modelos ficam em um volume Docker persistente.
- `app`: Python 3.12.16, CrewAI e Gradio.

Um serviço temporário `modelo-init` aguarda o Ollama e baixa `qwen2.5:3b` se ainda não estiver no volume. A aplicação só inicia depois que essa preparação terminar.

## Requisitos no Windows

- Docker Desktop instalado e iniciado, usando o backend WSL 2.
- VS Code com terminal PowerShell.
- Conexão com a internet na primeira execução para baixar imagens, pacotes e o modelo.

Não é necessário instalar Python nem Ollama no Windows.

## Iniciar

Na pasta que contém `compose.yaml`:

```powershell
docker compose config
docker compose up --build -d
```

A primeira execução baixa as imagens e o modelo. O download do modelo pode demorar e ocupa espaço no volume `ollama_data`.

Acompanhe a inicialização:

```powershell
docker compose ps
docker compose logs -f ollama
docker compose logs -f modelo-init
docker compose logs -f app
```

Abra a interface em:

http://localhost:7860

## Testar o modelo e o CrewAI

```powershell
docker compose exec ollama ollama list
docker compose run --rm app python --version
docker compose run --rm app python testar_ollama.py
```

## Executar pelo terminal

```powershell
docker compose run --rm app python -m agente "Explique polimorfismo com um exemplo em Java."
```

Agente inicial (SOLID):

```powershell
docker compose run --rm app python primeiro_agente.py "O que é o princípio da Responsabilidade Única?"
```

## Trocar o modelo

Edite `.env`, alterando `OLLAMA_MODEL`. Por exemplo:

```env
OLLAMA_MODEL=qwen2.5:3b
```

Depois execute novamente:

```powershell
docker compose up --build -d
```

O serviço `modelo-init` baixa o novo modelo para o volume persistente, caso ainda não exista.

## Encerrar e preservar modelos

```powershell
docker compose down
```

Isso remove os containers e a rede, mas preserva os modelos no volume `ollama_data`.

Para apagar também os modelos baixados:

```powershell
docker compose down -v
```

## GPU NVIDIA (opcional)

O modo padrão executa o Ollama em CPU. Para usar uma GPU NVIDIA, é necessário Docker Desktop com backend WSL 2, Windows atualizado, driver NVIDIA compatível e kernel WSL atualizado. Consulte a documentação do Docker Desktop para GPU no Windows.

Com os pré-requisitos atendidos, use o arquivo complementar:

```powershell
docker compose -f compose.yaml -f compose.nvidia.yaml up --build -d
```

Se a reserva de GPU falhar, volte ao comando padrão sem `compose.nvidia.yaml`.

## Como a aplicação conecta ao Ollama

Na rede interna criada pelo Compose, o host do servidor é `ollama`:

- API Ollama: `http://ollama:11434`
- API OpenAI-compatível: `http://ollama:11434/v1`

O helper `agente/llm.py` centraliza a configuração do LLM. Todos os agentes recebem a mesma instância configurada com `custom_openai=True`, sem usar o caminho LiteLLM do prefixo `ollama/`.
