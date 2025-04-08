from ninja import Schema
from typing import Optional, List
from datetime import datetime


class BaseSchema(Schema):
    """Schema base para todos os schemas que precisam de ID"""

    id: int


class TimestampedSchema(BaseSchema):
    """Schema base para todos os schemas que precisam de data de criação"""

    data_criacao: datetime


class UserSchema(BaseSchema):
    username: str
    role: str


class BaseProvaSchema(Schema):
    titulo: str
    descricao: Optional[str] = None


class ProvaIn(BaseProvaSchema):
    pass


class ProvaOut(BaseProvaSchema, TimestampedSchema):
    pass


class BaseQuestaoSchema(Schema):
    enunciado: str
    prova_id: int


class QuestaoIn(BaseQuestaoSchema):
    pass


class QuestaoOut(BaseQuestaoSchema, BaseSchema):
    pass


class BaseEscolhaSchema(Schema):
    texto: str
    is_correta: bool
    questao_id: int


class EscolhaIn(BaseEscolhaSchema):
    pass


class EscolhaOut(BaseEscolhaSchema, BaseSchema):
    pass


class BaseInscricaoSchema(Schema):
    participante_id: int
    prova_id: int


class InscricaoIn(BaseInscricaoSchema):
    pass


class InscricaoOut(BaseInscricaoSchema, TimestampedSchema):
    pass


class BaseRespostaSchema(Schema):
    inscricao_id: int
    questao_id: int
    escolha_id: int


class RespostaIn(BaseRespostaSchema):
    pass


class RespostaOut(BaseRespostaSchema, TimestampedSchema):
    corrigida: bool
    correta: Optional[bool]
