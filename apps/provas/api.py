from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Router, Query, Schema
from typing import List
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from apps.provas import models, schemas, tasks


api = NinjaAPI()

# Dependências JWT
import jwt
from django.conf import settings
from ninja.security import HttpBearer


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

# CRUD para Provas
prova_router = Router()


@prova_router.get("/", response=List[schemas.ProvaOut])
@method_decorator(cache_page(60), name="dispatch")
def list_provas(
    request,
    search: str = Query("", description="Buscar por título"),
    ordering: str = Query("id"),
    page: int = Query(1),
    page_size: int = Query(10),
):
    """
    Listar provas
    """
    qs = models.Prova.objects.all()
    if search:
        qs = qs.filter(titulo__icontains=search)
    qs = qs.order_by(ordering)
    paginator = Paginator(qs, page_size)
    provas = paginator.get_page(page)
    return list(provas)


@prova_router.post("/", response=schemas.ProvaOut, auth=auth)
def create_prova(request, payload: schemas.ProvaIn):
    """
    Criar prova
    """
    prova = models.Prova.objects.create(**payload.dict())
    return prova


@prova_router.get("/{prova_id}", response=schemas.ProvaOut)
def get_prova(request, prova_id: int):
    """
    Obter prova por ID
    """
    prova = get_object_or_404(models.Prova, id=prova_id)
    return prova


@prova_router.put("/{prova_id}", response=schemas.ProvaOut, auth=auth)
def update_prova(request, prova_id: int, payload: schemas.ProvaIn):
    """
    Atualiza prova por ID
    """
    prova = get_object_or_404(models.Prova, id=prova_id)
    for attr, value in payload.dict().items():
        setattr(prova, attr, value)
    prova.save()
    return prova


@prova_router.delete("/{prova_id}", auth=auth)
def delete_prova(request, prova_id: int):
    """
    Deleta prova
    """
    prova = get_object_or_404(models.Prova, id=prova_id)
    prova.delete()
    return {"success": True}


# TODO: Registre outros routers para Questao, Escolha, Inscricao e Resposta seguindo o mesmo padrão.
# TODO: Em especial, nos endpoints de Resposta, verifique se o usuário autenticado (obtido via JWTBearer)
# TODO: é o dono da inscrição, garantindo o controle de acesso.


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


# Registro da rota de provas
api.add_router("/provas/", prova_router)

# TODO: Verifica se o usuário autenticado é o dono da inscrição
