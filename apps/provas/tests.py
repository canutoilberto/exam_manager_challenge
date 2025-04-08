from django.test import TestCase
from django.urls import reverse
from apps.provas.models import Prova, User
import jwt
from django.conf import settings


# Create your tests here.
class ProvaAPITest(TestCase):
    def setUp(self):
        # Cria um usuário administrador para autenticação
        self.admin_user = User.objects.create_user(
            username="admin", password="admin123", role="ADMINISTRADOR"
        )
        self.token = jwt.encode(
            {"user_id": self.admin_user.id}, settings.SECRET_KEY, algorithm="HS256"
        )
        self.auth_header = f"Bearer {self.token}"

    def test_create_prova(self):
        url = "/api/provas/"
        data = {
            "titulo": "Prova de Matemática",
            "descricao": "Teste de lógica e números",
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["titulo"], "Prova de Matemática")

    # TODO: Crie testes para listagem, edição, exclusão, etc.
