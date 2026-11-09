FATOS_MEDIATOR = """
FATOS DE REFERÊNCIA - GoF Mediator
- Categoria: padrão comportamental do catálogo GoF.
- Intenção: encapsular como um conjunto de objetos interage, promovendo baixo
  acoplamento entre colegas que, de outra forma, conheceriam uns aos outros.
- Estrutura típica: Mediator define a interface de comunicação; ConcreteMediator
  coordena colegas concretos; Colleague conhece o mediador e envia eventos a ele.
- O mediador centraliza regras de colaboração. Os colegas não devem implementar
  diretamente a coordenação entre todos os demais colegas.
- Benefícios: reduz referências e dependências diretas entre colegas e concentra
  a coordenação em um lugar.
- Custos: o mediador pode acumular responsabilidades, tornar-se complexo e virar
  um objeto central difícil de manter. O padrão não elimina dependências: move a
  coordenação para o mediador.
- Use quando muitos objetos colaboram de forma complexa e mudanças nas relações
  entre eles causam dependências difíceis de administrar. Evite quando a
  colaboração é simples ou o mediador apenas repassa chamadas sem benefício.
- Exemplo didático: uma sala de bate-papo encaminha mensagens entre usuários;
  cada usuário conhece a sala, e a sala aplica a regra de distribuição.
- Comparação: Observer descreve principalmente uma relação de publicação e
  assinatura de notificações. Mediator centraliza a coordenação de interações
  entre colegas. Eles podem ser combinados, mas não são sinônimos.
- Participantes apresentados neste projeto: Mediator, ConcreteMediator,
  Colleague e ConcreteColleague. Variantes podem nomear ou organizar os papéis
  de outra forma; não declare que toda implementação precisa ter exatamente
  essas classes.
""".strip()

EXEMPLO_JAVA = r'''import java.util.ArrayList;
import java.util.List;

interface Mediator {
    void registrar(Usuario usuario);
    void enviar(Usuario origem, String mensagem);
}

final class SalaDeChat implements Mediator {
    private final List<Usuario> usuarios = new ArrayList<>();

    public void registrar(Usuario usuario) { usuarios.add(usuario); }

    public void enviar(Usuario origem, String mensagem) {
        for (Usuario destino : usuarios) {
            if (destino != origem) destino.receber(origem.nome() + ": " + mensagem);
        }
    }
}

final class Usuario {
    private final String nome;
    private final Mediator sala;

    Usuario(String nome, Mediator sala) { this.nome = nome; this.sala = sala; }
    String nome() { return nome; }
    void enviar(String mensagem) { sala.enviar(this, mensagem); }
    void receber(String mensagem) { System.out.println(nome + " recebeu: " + mensagem); }
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
}'''

EXEMPLOS_DIDATICOS = """
CENÁRIOS DIDÁTICOS POSSÍVEIS (são exemplos ilustrativos, não afirmações de que
são exemplos canônicos do livro GoF):
- Diálogo de formulário: caixas de texto, botões e seleções notificam um
  DialogMediator; o diálogo decide habilitar campos ou botões. Os widgets não
  chamam diretamente uns aos outros.
- Casa inteligente: sensor de movimento e dispositivos de luz notificam um
  SmartHomeMediator; a central aplica uma regra como acender a luz quando há
  movimento. Os dispositivos não coordenam diretamente entre si.
- Checkout: seletores de entrega, pagamento e resumo notificam um
  CheckoutMediator; ele atualiza opções e totais segundo as escolhas. Os
  componentes não mantêm dependências diretas entre todos os demais.
- Sala de bate-papo: usuários enviam mensagens a uma sala que as distribui.

Use esses cenários como sementes para exemplos novos. Ao adaptar ou criar um
exemplo, deixe claro que é didático/hipotético. Preserve sempre esta estrutura:
colegas enviam eventos ao mediador; o mediador aplica uma regra explícita e
coordena a reação; colegas não chamam diretamente uns aos outros. Não diga que
um cenário criado pelo tutor é um exemplo oficial do GoF.
""".strip()

