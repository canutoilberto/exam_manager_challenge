from django_elasticsearch_dsl import Document, Index
from apps.provas.models import Prova


provas_index = Index("provas")
provas_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
)


@provas_index.doc_type
class ProvaDocument(Document):
    class Django:
        model = Prova
        fields = ["id", "titulo", "descricao", "data_criacao"]
