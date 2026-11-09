# Exemplo Java: sala de bate-papo com Mediator

Neste exemplo, `Usuario` é um colega. Ele envia mensagens ao contrato
`Mediator` e não percorre diretamente os outros usuários. `SalaDeChat` é o
mediador concreto e aplica a regra de encaminhar a mensagem aos demais
participantes.

```java
import java.util.ArrayList;
import java.util.List;

interface Mediator {
    void registrar(Usuario usuario);
    void enviar(Usuario origem, String mensagem);
}

final class SalaDeChat implements Mediator {
    private final List<Usuario> usuarios = new ArrayList<>();

    public void registrar(Usuario usuario) {
        usuarios.add(usuario);
    }

    public void enviar(Usuario origem, String mensagem) {
        for (Usuario destino : usuarios) {
            if (destino != origem) {
                destino.receber(origem.nome() + ": " + mensagem);
            }
        }
    }
}

final class Usuario {
    private final String nome;
    private final Mediator sala;

    Usuario(String nome, Mediator sala) {
        this.nome = nome;
        this.sala = sala;
    }

    String nome() {
        return nome;
    }

    void enviar(String mensagem) {
        sala.enviar(this, mensagem);
    }

    void receber(String mensagem) {
        System.out.println(nome + " recebeu: " + mensagem);
    }
}

public class ExemploMediator {
    public static void main(String[] args) {
        Mediator sala = new SalaDeChat();
        Usuario ana = new Usuario("Ana", sala);
        Usuario bia = new Usuario("Bia", sala);
        sala.registrar(ana);
        sala.registrar(bia);
        ana.enviar("Oi!");
    }
}
```

O exemplo é propositalmente simples. Uma implementação real pode acrescentar
salas, regras de privacidade e tratamento de usuários duplicados; esses detalhes
de produto não fazem parte da intenção essencial do padrão.
