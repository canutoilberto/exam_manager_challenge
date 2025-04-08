from django_elasticsearch_dsl import Document, Index, fields
from apps.provas.models import Prova, Questao

# Configuração do índice de provas
provas_index = Index("provas")
provas_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
)

# Configuração do índice de questões
questoes_index = Index("questoes")
questoes_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
)


@provas_index.doc_type
class ProvaDocument(Document):
    class Django:
        model = Prova
        fields = ["id", "titulo", "descricao", "data_criacao"]


@questoes_index.doc_type
class QuestaoDocument(Document):
    prova = fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "titulo": fields.TextField(),
        }
    )

    class Django:
        model = Questao
        fields = ["id", "enunciado"]

    def get_queryset(self):
        """Incluir informações da prova relacionada"""
        return super().get_queryset().select_related("prova")
