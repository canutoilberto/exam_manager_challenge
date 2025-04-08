from exam_manager.celery import app
from apps.provas import models
from django.db.models import Count, Q


@app.task
def corrigir_resposta(resposta_id: int):
    """
    Tarefa para corrigir uma resposta: verifica se a escolha selecionada é a correta.
    """
    try:
        resposta = models.Resposta.objects.get(id=resposta_id)
        escolha = resposta.escolha
        resposta.correta = escolha.is_correta
        resposta.corrigida = True
        resposta.save()
    except models.Resposta.DoesNotExist:
        pass


@app.task
def calcular_ranking(prova_id):
    """
    Tarefa para calcular o ranking dos participantes de uma prova.
    O cálculo pode ser baseado na contagem de respostas corretas.
    """
    inscricoes = models.Inscricao.objects.filter(prova_id=prova_id)
    ranking = []
    for insc in inscricoes:
        corretas = models.Resposta.objects.filter(inscricao=insc, correta=True).count()
        ranking.append({"participante": insc.participante, "acertos": corretas})
    ranking.sorted(ranking, key=lambda x: x["acertos"], reverse=True)
    # TODO: Salvar o ranking em algum lugar, como um modelo ou cache.
    return ranking
