"""
UI Automation — Login Flow
Testa o fluxo de login via browser usando Playwright + Pytest.
"""

import pytest
from playwright.sync_api import Page, expect


BASE_URL = "http://localhost:3000"


@pytest.fixture(autouse=True)
def ir_para_login(page: Page):
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")


# ─────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────

def fazer_login(page: Page, email: str, senha: str):
    page.get_by_label("Email").fill(email)
    page.get_by_label("Senha").fill(senha)
    page.get_by_role("button", name="Entrar").click()


# ─────────────────────────────────────────
# Testes
# ─────────────────────────────────────────

class TestLoginSucesso:

    def test_login_valido_redireciona_para_dashboard(self, page: Page):
        fazer_login(page, "iron@teste.com", "Senha@123")
        expect(page).to_have_url(f"{BASE_URL}/dashboard")
        expect(page.get_by_text("Bem-vindo")).to_be_visible()

    def test_nome_usuario_aparece_no_header(self, page: Page):
        fazer_login(page, "iron@teste.com", "Senha@123")
        expect(page.get_by_test_id("user-name")).to_contain_text("Iron")


class TestLoginFalha:

    def test_senha_errada_exibe_mensagem_de_erro(self, page: Page):
        fazer_login(page, "iron@teste.com", "senha_errada")
        expect(page.get_by_role("alert")).to_be_visible()
        expect(page.get_by_role("alert")).to_contain_text("Credenciais inválidas")

    def test_usuario_inexistente_exibe_erro_generico(self, page: Page):
        """
        Erro deve ser genérico para não vazar se email existe.
        NÃO deve dizer "email não encontrado" — isso é uma vulnerabilidade.
        """
        fazer_login(page, "nao.existe@teste.com", "qualquer")
        alerta = page.get_by_role("alert")
        expect(alerta).to_be_visible()
        expect(alerta).not_to_contain_text("não encontrado")
        expect(alerta).not_to_contain_text("not found")

    def test_campos_vazios_exibem_validacao(self, page: Page):
        page.get_by_role("button", name="Entrar").click()
        expect(page.get_by_text("Campo obrigatório")).to_have_count(2)

    def test_url_nao_muda_apos_login_com_falha(self, page: Page):
        fazer_login(page, "iron@teste.com", "errada")
        expect(page).to_have_url(f"{BASE_URL}/login")


class TestAcessibilidade:

    def test_campos_tem_labels_acessiveis(self, page: Page):
        """Garante que leitores de tela conseguem identificar os campos."""
        email_input = page.get_by_label("Email")
        senha_input = page.get_by_label("Senha")
        expect(email_input).to_be_visible()
        expect(senha_input).to_be_visible()

    def test_navegacao_por_tab(self, page: Page):
        page.keyboard.press("Tab")  # foca no email
        page.keyboard.type("iron@teste.com")
        page.keyboard.press("Tab")  # vai para senha
        page.keyboard.type("Senha@123")
        page.keyboard.press("Tab")  # vai para botão
        page.keyboard.press("Enter")
        expect(page).to_have_url(f"{BASE_URL}/dashboard")

    def test_botao_submit_tem_texto_descritivo(self, page: Page):
        botao = page.get_by_role("button", name="Entrar")
        expect(botao).to_be_visible()
        expect(botao).to_be_enabled()
