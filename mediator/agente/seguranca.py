import re
import unicodedata


class EntradaInvalida(ValueError):
    """Entrada vazia ou maior que o limite operacional do chat."""


def normalizar(texto: str) -> str:
    sem_acentos = unicodedata.normalize("NFKD", texto)
    return "".join(caractere for caractere in sem_acentos if not unicodedata.combining(caractere)).lower()


def validar_pergunta(pergunta: str) -> str:
    if not isinstance(pergunta, str) or not pergunta.strip():
        raise EntradaInvalida("Digite uma pergunta antes de enviar.")
    pergunta = pergunta.strip()
    if len(pergunta) > 2000:
        raise EntradaInvalida("A pergunta deve ter no máximo 2.000 caracteres.")
    return pergunta


def _pedido_de_inventar_padrao(texto: str) -> bool:
    texto = normalizar(texto)
    verbo_criacao = r"\b(invente|inventar|crie|criar|imagine|imaginar)\b"
    nome_padrao = r"\b(padrao|design pattern)\b"
    return bool(re.search(verbo_criacao + r".{0,70}" + nome_padrao, texto))


def _pedido_de_solucao_pronta(texto: str) -> bool:
    texto = normalizar(texto)
    trecho_pronto = r"\b(codigo|solucao|trabalho|projeto)\b.{0,50}\b(pronto|completo|completa|inteiro|inteira|final)\b"
    trecho_invertido = r"\b(pronto|pronta|completo|completa|inteiro|inteira)\b.{0,50}\b(codigo|solucao|trabalho|projeto)\b"
    pedido_direto = r"\b(me entregue|me de|me forneca|faca para mim|faça para mim)\b"
    return bool(
        re.search(trecho_pronto, texto)
        or re.search(trecho_invertido, texto)
        or (re.search(pedido_direto, texto) and re.search(r"\b(codigo|solucao)\b", texto) and re.search(r"\b(completo|completa|pronto|pronta)\b", texto))
    )


def resposta_de_seguranca(pergunta: str) -> str | None:
    if _pedido_de_inventar_padrao(pergunta):
        return (
            "Não vou apresentar um padrão inventado como se fosse parte do catálogo GoF. "
            "Posso explicar o Mediator real: ele centraliza a coordenação entre objetos "
            "colegas. Quer comparar essa ideia com Observer?"
        )

    if _pedido_de_solucao_pronta(pergunta):
        return (
            "Posso ajudar você a construir a solução por etapas, revisar uma tentativa "
            "ou explicar como o Mediator organiza a colaboração. Para começar, quais "
            "objetos do seu problema precisam coordenar ações?"
        )

    return None
