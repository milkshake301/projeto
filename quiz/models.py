from django.db import models


class Question(models.Model):
    text = models.TextField("situação")
    explanation = models.TextField("explicação")
    order = models.PositiveSmallIntegerField("ordem", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "pergunta"
        verbose_name_plural = "perguntas"

    def __str__(self):
        return self.text[:60]


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    text = models.CharField("resposta", max_length=300)
    is_correct = models.BooleanField("correta", default=False)

    class Meta:
        ordering = ["id"]
        verbose_name = "alternativa"
        verbose_name_plural = "alternativas"

    def __str__(self):
        return self.text[:60]
