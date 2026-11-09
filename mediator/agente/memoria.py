from dataclasses import dataclass

@dataclass(frozen=True)
class Turno:
    pergunta: str
    resposta: str

class MemoriaConversa:
    def __init__(self, max_turnos: int = 3) -> None:
        self.max_turnos = max(1, max_turnos)
        self._turnos: list[Turno] = []

    def registrar(self, pergunta: str, resposta: str) -> None:
        self._turnos.append(Turno(pergunta=pergunta, resposta=resposta))
        self._turnos = self._turnos[-self.max_turnos :]

    def como_contexto(self) -> str:
        if not self._turnos:
            return "Ainda não houve turnos anteriores nesta sessão."

        partes = []
        for indice, turno in enumerate(self._turnos, start=1):
            partes.append(
                f"Turno anterior {indice}\n"
                f"Estudante: {turno.pergunta}\n"
                f"Tutor: {turno.resposta}"
            )
        return "\n\n".join(partes)
