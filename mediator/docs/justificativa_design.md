# Justificativa das decisões de design

## Objetivo pedagógico

O sistema foi delimitado ao padrão Mediator para favorecer explicações
consistentes em uma sessão curta de aprendizagem. O objetivo não é substituir o
material da disciplina nem catalogar todos os padrões GoF. O tutor ajuda o
estudante a relacionar quatro elementos: a intenção do padrão, o tipo de
colaboração que ele organiza, os participantes comuns e os custos de concentrar
a coordenação em um objeto mediador.

A explicação usa como ponto de partida a situação em que vários objetos precisam
cooperar. Sem mediador, cada colega pode manter referências e regras diretas para
os demais, tornando alterações na colaboração difíceis de acompanhar. Com
Mediator, os colegas encaminham eventos ao mediador, que conhece as regras de
coordenação. A conversa também apresenta o custo dessa solução: a coordenação
fica concentrada e pode fazer o mediador crescer demais. Essa apresentação dos
trade-offs ajuda a evitar que o padrão apareça como solução universal.

## Divisão de responsabilidades

A aplicação organiza o trabalho em três agentes CrewAI sequenciais. O primeiro,
Tutor conceitual, apresenta a intenção, o problema, os participantes e as
consequências. O segundo, Exemplificador Java, relaciona a explicação a um
cenário pequeno e reconhecível: usuários de uma sala de bate-papo enviam
mensagens à sala, e a sala decide como encaminhá-las. Quando o estudante pede
outro exemplo, o agente escolhe entre sementes variadas (diálogo de formulário,
casa inteligente e checkout) ou formula um cenário didático novo, evitando
reutilizar os casos da memória. O terceiro, Inquiridor e
revisor, detecta equívocos, revisa o texto anterior com uma referência factual,
fornece feedback e sugere uma pergunta curta para verificar compreensão.

A especificação permite diferentes distribuições de papéis e sugere quatro
agentes no anexo. Aqui o diagnóstico e a revisão final ficam juntos em um agente
para reduzir uma invocação do Qwen por turno. Essa redução é relevante para o
modelo 3B escolhido e para computadores com recursos limitados. As três tarefas
continuam explícitas e ligadas por `context` na ordem Tutor → Exemplificador →
Inquiridor. Nenhum agente delega para uma equipe nova, reduzindo chamadas
imprevisíveis.

## Estratégia pedagógica

O sistema combina explicação direta, exemplificação e prática curta. Uma dúvida
conceitual recebe uma explicação concisa e um trecho de Java; ao final, o
inquiridor propõe uma pergunta de checagem sem revelar sua resposta. Quando o
estudante responde em um turno posterior, a memória permite que o agente
revisor retome a tentativa e dê feedback. O modelo não deve entregar uma
aplicação inteira como atalho para a atividade: a regra de resposta orienta a
construção por etapas, a análise de uma tentativa ou a implementação de uma
parte específica.

Esse formato apoia aprendizagem ativa sem transformar cada interação em uma
prova. A pergunta final serve como próximo passo, e o estudante pode mudar de
assunto ou pedir uma comparação. A comparação com Observer é incluída porque
essa confusão é frequente no roteiro da atividade: Observer descreve uma
relação de publicação e assinatura; Mediator concentra a coordenação entre
colegas. A resposta explica diferença de intenção sem afirmar que as soluções
são incompatíveis.

## Memória e estado

`MemoriaConversa` armazena até três pares de pergunta e resposta enquanto o
processo interativo está aberto. Na próxima chamada, esse histórico é inserido
explicitamente na tarefa, em vez de depender de uma memória implícita do
framework. Assim, o uso de memória é simples de inspecionar, delimitado e
independente de banco vetorial, serviço externo ou armazenamento remoto.

O histórico é transitório: iniciar um novo processo começa outra conversa, e
nenhum texto é salvo em disco. A chamada de pergunta única exigida pelo
contrato `python -m agente "pergunta"` atende à automação de cenários; a CLI sem
argumentos abre um laço que atende a requisito de coerência entre vários
turnos. A separação reduz complexidade operacional e evita armazenar dados do
estudante sem necessidade. O limite configurável também restringe o tamanho de
contexto enviado ao modelo.

## Regras anti-alucinação

O conhecimento do tutor é ancorado em uma referência local com intenção,
categoria, participantes típicos, custos, condições de uso e comparação com
Observer. O prompt instrui os agentes a usar essa referência, a dizer que não
sabem quando ela não sustentar uma afirmação e a não tratar nomes de classes
como obrigatórios em todas as variantes. As sementes de cenário são marcadas
como ilustrações hipotéticas, não como exemplos oficiais do GoF. Cada cenário
precisa mostrar colegas notificando o mediador, uma regra central de coordenação
e uma reação mediada; isso dá variedade sem alterar a definição do padrão.

Há também dois controles determinísticos antes do LLM: pergunta vazia ou acima
de 2.000 caracteres é rejeitada, e pedidos explícitos para inventar um padrão
ou entregar uma solução completa recebem orientação segura sem invocar o
modelo. O terceiro agente revisa a saída dos outros dois contra os fatos-base.
Esses controles tornam os comportamentos avaliáveis, mas não provam a correção
de todas as respostas: uma regra textual pode não reconhecer formulações
ambíguas, e um revisor generativo ainda pode errar. Por isso, o roteiro de
validação inclui casos esperados e deve ser executado e registrado pela dupla.

## Modelo, custo e execução

O modelo padrão é `qwen2.5:3b` executado pelo Ollama no próprio computador, em
CPU por padrão. O cliente CrewAI usa a API local compatível com OpenAI, na rede
interna do Compose; a chave de texto `ollama` é apenas um valor local fictício
que satisfaz o cliente e não é credencial. Não existe endpoint de inferência em
nuvem nem chamada paga. A internet é usada para preparar imagens, bibliotecas e
pesos do modelo, conforme permitido pelo enunciado. O volume Docker mantém os
pesos para execuções seguintes.

O projeto separa CLI, segurança, memória, conhecimento, configuração LLM e
orquestração em módulos pequenos. O Compose mantém Ollama e aplicação em
containers separados; um serviço de inicialização espera pelo servidor e baixa
o modelo somente se necessário. A documentação explica os comandos de uma
pergunta, do chat interativo, do modo CPU e da opção de GPU NVIDIA.

## Como validar as decisões

Antes da entrega, os integrantes devem revisar os fatos e o exemplo com a
bibliografia da disciplina, rodar os cenários de `roteiro_validacao.md` com o
modelo local, registrar latência aproximada, correção e utilidade no caderno de
evidências e completar o mini-relatório com a máquina realmente utilizada.
Nenhuma resposta de teste ou experiência da dupla foi inventada nesta versão.
