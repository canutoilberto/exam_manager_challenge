from ninja import Schema
from typing import Optional, List
from datetime import datetime


class UserSchema(Schema):
    id: int
    username: str
    role: str


class ProvaIn(Schema):
    titulo: str
    descricao: Optional[str] = None


class ProvaOut(Schema):
    id: int
    titulo: str
    descricao: Optional[str] = None
    data_criacao: datetime


class QuestaoIn(Schema):
    prova_id: int
    enunciado: str


class QuestaoOut(Schema):
    id: int
    prova_id: int
    enunciado: str


class EscolhaIn(Schema):
    questao_id: int
    texto: str
    is_correta: bool


class EscolhaOut(Schema):
    id: int
    questao_id: int
    texto: str
    is_correta: bool


class InscricaoIn(Schema):
    participante_id: int
    prova_id: id


class IscricaoOut(Schema):
    id: int
    participante_id: int
    prova_id: int
    data_inscricao: datetime


class RespostaIn(Schema):
    inscricao_id: int
    questao_id: int
    escolha_id: int


class RespostaOut(Schema):
    id: int
    inscricao_id: int
    questao_id: int
    escolha_id: int
    data_resposta: datetime
    corrigida: bool
    correta: Optional[bool]
