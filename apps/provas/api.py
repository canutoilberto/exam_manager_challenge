from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Router, Query, Schema
from typing import List, Type, TypeVar, Generic
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from apps.provas import models, schemas, tasks
from django.db.models import Model


api = NinjaAPI()

# Dependências JWT
import jwt
from django.conf import settings
from ninja.security import HttpBearer

T = TypeVar("T", bound=Model)


class JWTBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            from apps.provas.models import User

            user = User.objects.get(id=user_id)
            return user
        except Exception:
            return None


auth = JWTBearer()


class BaseCRUDRouter(Generic[T]):
    """Classe base para operações CRUD"""

    def __init__(
        self,
        model: Type[T],
        schema_in: Type[Schema],
        schema_out: Type[Schema],
        router: Router,
        search_field: str = "titulo",
    ):
        self.model = model
        self.schema_in = schema_in
        self.schema_out = schema_out
        self.router = router
        self.search_field = search_field
        self._register_routes()

    def _register_routes(self):
        @self.router.get(
            "/",
            response=List[self.schema_out],
            operation_id=f"{self.model.__name__.lower()}_list",
        )
        def list_items(
            request,
            search: str = Query("", description=f"Buscar por {self.search_field}"),
            ordering: str = Query("id"),
            page: int = Query(1),
            page_size: int = Query(10),
        ):
            qs = self.model.objects.all()
            if search and hasattr(self.model, self.search_field):
                qs = qs.filter(**{f"{self.search_field}__icontains": search})
            qs = qs.order_by(ordering)
            paginator = Paginator(qs, page_size)
            items = paginator.get_page(page)
            return list(items)

        @self.router.post(
            "/",
            response=self.schema_out,
            auth=auth,
            operation_id=f"{self.model.__name__.lower()}_create",
        )
        def create_item(request, payload: self.schema_in):
            item = self.model.objects.create(**payload.dict())
            return item

        @self.router.get(
            "/{item_id}",
            response=self.schema_out,
            operation_id=f"{self.model.__name__.lower()}_get",
        )
        def get_item(request, item_id: int):
            item = get_object_or_404(self.model, id=item_id)
            return item

        @self.router.put(
            "/{item_id}",
            response=self.schema_out,
            auth=auth,
            operation_id=f"{self.model.__name__.lower()}_update",
        )
        def update_item(request, item_id: int, payload: self.schema_in):
            item = get_object_or_404(self.model, id=item_id)
            for attr, value in payload.dict().items():
                setattr(item, attr, value)
            item.save()
            return item

        @self.router.delete(
            "/{item_id}",
            auth=auth,
            operation_id=f"{self.model.__name__.lower()}_delete",
        )
        def delete_item(request, item_id: int):
            item = get_object_or_404(self.model, id=item_id)
            item.delete()
            return {"success": True}


# Instanciando routers
prova_router = Router()
questao_router = Router()
escolha_router = Router()
inscricao_router = Router()

# Registrando CRUDs
prova_crud = BaseCRUDRouter(
    model=models.Prova,
    schema_in=schemas.ProvaIn,
    schema_out=schemas.ProvaOut,
    router=prova_router,
    search_field="titulo",
)

questao_crud = BaseCRUDRouter(
    model=models.Questao,
    schema_in=schemas.QuestaoIn,
    schema_out=schemas.QuestaoOut,
    router=questao_router,
    search_field="enunciado",
)

escolha_crud = BaseCRUDRouter(
    model=models.Escolha,
    schema_in=schemas.EscolhaIn,
    schema_out=schemas.EscolhaOut,
    router=escolha_router,
    search_field="texto",
)

inscricao_crud = BaseCRUDRouter(
    model=models.Inscricao,
    schema_in=schemas.InscricaoIn,
    schema_out=schemas.InscricaoOut,
    router=inscricao_router,
)


# Endpoint para envio de respostas com disparo de job de correção
@api.post("/respostas", response=schemas.RespostaOut, auth=auth)
def submit_resposta(request, payload: schemas.RespostaIn):
    """
    Envia resposta e dispara job de correção
    """
    # Verifica se o usuário autenticado é o dono da inscrição
    inscricao = get_object_or_404(
        models.Inscricao, id=payload.inscricao_id, participante=request.auth
    )
    resposta, created = models.Resposta.objects.update_or_create(
        inscricao=inscricao,
        questao_id=payload.questao_id,
        defaults={"escolha_id": payload.escolha_id},
    )
    # Dispara o job assíncrono de correção
    tasks.corrigir_resposta.delay(resposta.id)
    return resposta


# Registro das rotas
api.add_router("/provas/", prova_router)
api.add_router("/questoes/", questao_router)
api.add_router("/escolhas/", escolha_router)
api.add_router("/inscricoes/", inscricao_router)
