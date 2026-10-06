from django.core.management.base import BaseCommand

from quiz.models import Choice, Question

# (situação, explicação, índice da correta, alternativas)
DATA = [
    ("Um print de uma foto constrangedora da Lu está circulando no grupo da turma. Todo mundo comenta e ri.",
     "Quem repassa o conteúdo também faz parte da agressão, e cada compartilhamento amplia a exposição. O que mais ajuda é interromper a cadeia, apoiar a pessoa e pedir ajuda a um adulto de confiança.",
     1, ["Encaminho só para uma amiga, ninguém vai saber",
         "Não compartilho, mando uma mensagem de apoio para a Lu e aviso um adulto de confiança",
         "Fico quieto: não fui eu que postei, então não é problema meu"]),
    ("Qual destas situações é cyberbullying?",
     "Cyberbullying é a agressão repetida, feita por meios digitais, com a intenção de humilhar ou machucar. Uma discordância ou uma briga pontual que se resolve não tem esse padrão.",
     2, ["Dois amigos discutem num chat e fazem as pazes no dia seguinte",
         "Uma pessoa discorda educadamente da sua opinião num comentário",
         "Alguém cria um perfil falso para ridicularizar uma colega todos os dias"]),
    ("Você começou a receber mensagens ofensivas de um número desconhecido. Qual é a melhor primeira atitude?",
     "Responder costuma alimentar a agressão. Os prints servem de prova, bloquear corta o contato e contar a alguém de confiança evita que você carregue isso sozinho.",
     0, ["Não responder, guardar os prints, bloquear o contato e contar para alguém de confiança",
         "Responder à altura para a pessoa aprender",
         "Apagar tudo e fingir que nada aconteceu"]),
    ("Depois de postar uma piada sobre o sotaque de um colega, alguém diz: “foi só brincadeira”. Isso muda alguma coisa?",
     "Brincadeira boa diverte todo mundo, inclusive quem é o alvo. Quando uma parte ri e a outra sofre, é hora de parar e pedir desculpas.",
     2, ["Sim, se todo mundo riu, deixa de ser problema",
         "Sim, entre amigos pode tudo",
         "Não: se a pessoa se sentiu ferida, a intenção não apaga o dano"]),
    ("Você viu um colega sendo atacado nos comentários de um vídeo. O que mais ajuda?",
     "Quem presencia tem um papel importante. Denunciar e apoiar a vítima em particular mostram que ela não está sozinha, sem alimentar o ataque.",
     0, ["Denunciar os comentários e mandar uma mensagem de apoio em particular",
         "Curtir os comentários para não virar o próximo alvo",
         "Ficar em silêncio: se mais gente entrar, piora"]),
    ("Sobre denunciar conteúdo ofensivo nas redes, o que é verdade?",
     "Quase toda plataforma permite denunciar posts, comentários e perfis, e qualquer usuário pode fazer isso. Guarde prints e links antes, para ter registro.",
     2, ["Só os pais ou responsáveis podem denunciar",
         "Denunciar não adianta, os perfis nunca são removidos",
         "As plataformas têm ferramentas de denúncia e o conteúdo que viola as regras pode ser removido"]),
    ("Um amigo parece isolado e triste desde que começou a ser xingado na internet. O que fazer?",
     "Muita gente demora a pedir ajuda. Ouvir sem minimizar já alivia, e se ele estiver muito mal, vale buscar apoio profissional ou ligar para o CVV, no 188.",
     1, ["Dizer que ele precisa ignorar, porque isso passa",
         "Conversar com calma, ouvir sem julgar e incentivar que ele procure um adulto de confiança",
         "Esperar ele pedir ajuda"]),
    ("No Brasil, o que a lei diz sobre cyberbullying?",
     "A Lei 14.811/2024 criou o crime de intimidação sistemática, inclusive na forma virtual. Além da esfera penal, a vítima pode buscar reparação por danos morais.",
     1, ["Não há regra nenhuma, só a escola pode punir",
         "Desde 2024, a intimidação sistemática virtual é crime (Lei 14.811)",
         "Só é crime se a vítima for maior de idade"]),
]


class Command(BaseCommand):
    help = "Cria as perguntas iniciais do quiz (use --reset para apagar as existentes)."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true")

    def handle(self, *args, **opts):
        if opts["reset"]:
            Question.objects.all().delete()
        if Question.objects.exists():
            self.stdout.write("Já existem perguntas. Use --reset para recriar.")
            return
        for order, (text, expl, right, choices) in enumerate(DATA, 1):
            q = Question.objects.create(text=text, explanation=expl, order=order)
            Choice.objects.bulk_create(
                Choice(question=q, text=t, is_correct=(i == right)) for i, t in enumerate(choices)
            )
        self.stdout.write(self.style.SUCCESS(f"{len(DATA)} perguntas criadas."))
