from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
ROLE_CHOICES = (
    ("ADMINISTRADOR", "Administrador"),
    ("PARTICIPANTE", "Participante"),
)


class TimestampedModel(models.Model):
    """Classe base para modelos que precisam de timestamp de criação"""

    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="PARTICIPANTE")

    def __str__(self):
        return self.username


class Prova(TimestampedModel):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.titulo


class Questao(models.Model):
    prova = models.ForeignKey(Prova, related_name="questoes", on_delete=models.CASCADE)
    enunciado = models.TextField()

    def __str__(self):
        return f"Questão {self.id} - {self.prova.titulo}"


class Escolha(models.Model):
    questao = models.ForeignKey(
        Questao, related_name="escolhas", on_delete=models.CASCADE
    )
    texto = models.CharField(max_length=300)
    is_correta = models.BooleanField(default=False)

    def __str__(self):
        return f"Escolha {self.id} para {self.questao.id}"


class Inscricao(TimestampedModel):
    participante = models.ForeignKey(
        User, limit_choices_to={"role": "PARTICIPANTE"}, on_delete=models.CASCADE
    )
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("participante", "prova"),)

    def __str__(self):
        return f"{self.participante.username} - {self.prova.titulo}"


class Resposta(TimestampedModel):
    inscricao = models.ForeignKey(
        Inscricao, related_name="respostas", on_delete=models.CASCADE
    )
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    escolha = models.ForeignKey(Escolha, on_delete=models.CASCADE)
    corrigida = models.BooleanField(default=False)
    correta = models.BooleanField(null=True)  # Será definida após correção

    class Meta:
        unique_together = (("inscricao", "questao"),)

    def __str__(self):
        return (
            f"Resposta de {self.inscricao.participante.username} na {self.questao.id}"
        )
