"""
API Tests — /api/users
Testa os endpoints de criação, leitura e deleção de usuários.
"""

import pytest
import requests
from uuid import uuid4

pytestmark = pytest.mark.api

BASE_URL = "http://localhost:3000/api"


@pytest.fixture(scope="module")
def auth_token():
    """Autentica e retorna token para os testes."""
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@teste.com",
        "password": "Admin@123"
    })
    assert response.status_code == 200, "Falha na autenticação para setup dos testes"
    return response.json()["token"]


@pytest.fixture
def headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def novo_usuario():
    unique_id = uuid4().hex[:8]
    return {
        "name": "Iron QA",
        "email": f"iron.qa.{unique_id}@teste.com",
        "role": "viewer"
    }


# ─────────────────────────────────────────
# GET /api/users
# ─────────────────────────────────────────

class TestListarUsuarios:

    def test_retorna_lista_de_usuarios(self, headers):
        r = requests.get(f"{BASE_URL}/users", headers=headers)
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_cada_usuario_tem_campos_obrigatorios(self, headers):
        r = requests.get(f"{BASE_URL}/users", headers=headers)
        campos = {"id", "name", "email", "role", "status"}
        for usuario in r.json():
            assert campos.issubset(usuario.keys()), \
                f"Usuário sem campos obrigatórios: {usuario}"

    def test_sem_token_retorna_401(self):
        r = requests.get(f"{BASE_URL}/users")
        assert r.status_code == 401

    def test_token_invalido_retorna_401(self):
        r = requests.get(f"{BASE_URL}/users",
                         headers={"Authorization": "Bearer token_invalido"})
        assert r.status_code == 401


# ─────────────────────────────────────────
# POST /api/users
# ─────────────────────────────────────────

class TestCriarUsuario:

    def test_cria_usuario_com_dados_validos(self, headers, novo_usuario):
        r = requests.post(f"{BASE_URL}/users", json=novo_usuario, headers=headers)
        assert r.status_code == 201
        data = r.json()
        assert data["email"] == novo_usuario["email"]
        assert "id" in data
        # Cleanup
        requests.delete(f"{BASE_URL}/users/{data['id']}", headers=headers)

    def test_email_duplicado_retorna_409(self, headers, novo_usuario):
        # Cria primeiro
        r1 = requests.post(f"{BASE_URL}/users", json=novo_usuario, headers=headers)
        assert r1.status_code == 201
        user_id = r1.json()["id"]
        # Tenta criar de novo com mesmo email
        r2 = requests.post(f"{BASE_URL}/users", json=novo_usuario, headers=headers)
        assert r2.status_code == 409
        assert "already exists" in r2.json().get("message", "").lower()
        # Cleanup
        requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)

    def test_email_invalido_retorna_422(self, headers):
        payload = {"name": "Teste", "email": "nao-eh-email", "role": "viewer"}
        r = requests.post(f"{BASE_URL}/users", json=payload, headers=headers)
        assert r.status_code == 422

    def test_campo_obrigatorio_ausente_retorna_422(self, headers):
        payload = {"name": "Sem Email"}  # falta email e role
        r = requests.post(f"{BASE_URL}/users", json=payload, headers=headers)
        assert r.status_code == 422

    def test_resposta_nao_expoe_senha(self, headers, novo_usuario):
        r = requests.post(f"{BASE_URL}/users", json=novo_usuario, headers=headers)
        assert r.status_code == 201
        data = r.json()
        assert "password" not in data
        assert "password_hash" not in data
        # Cleanup
        requests.delete(f"{BASE_URL}/users/{data['id']}", headers=headers)


# ─────────────────────────────────────────
# DELETE /api/users/:id
# ─────────────────────────────────────────

class TestDeletarUsuario:

    def test_deleta_usuario_existente(self, headers, novo_usuario):
        r = requests.post(f"{BASE_URL}/users", json=novo_usuario, headers=headers)
        user_id = r.json()["id"]
        r_del = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
        assert r_del.status_code == 204

    def test_usuario_inexistente_retorna_404(self, headers):
        r = requests.delete(f"{BASE_URL}/users/999999", headers=headers)
        assert r.status_code == 404

    def test_sem_permissao_retorna_403(self, auth_token):
        """Usuário com role viewer não pode deletar."""
        # Autentica como viewer
        r_login = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "viewer@teste.com",
            "password": "Viewer@123"
        })
        viewer_token = r_login.json().get("token")
        r = requests.delete(f"{BASE_URL}/users/1",
                            headers={"Authorization": f"Bearer {viewer_token}"})
        assert r.status_code == 403
