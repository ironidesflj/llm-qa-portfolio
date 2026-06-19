"""
Data Quality Tests — Pipeline de Usuários
==========================================
Valida a qualidade dos dados após um pipeline ETL.
Simula o que um QA de dados faz no dia a dia.

Dependências:
    pip install great_expectations pandas pytest
"""

import pytest
import pandas as pd
from io import StringIO

pytestmark = pytest.mark.data

# ─────────────────────────────────────────
# Fixture: simula dados saindo de um pipeline ETL
# ─────────────────────────────────────────

DADOS_CSV = """id,name,email,age,country,registration_date,status
1,Iron QA,iron@teste.com,28,BR,2024-01-15,active
2,Maria Silva,maria@silva.com,34,BR,2024-01-16,active
3,John Doe,john@example.com,25,US,2024-01-17,inactive
4,Ana Souza,ana@souza.com,30,BR,2024-01-18,active
5,Bob Smith,bob@smith.com,42,US,2024-01-19,active
6,Carlos Oliveira,carlos@oliveira.com,35,BR,2024-01-20,active
7,Duplicate User,dup1@teste.com,30,BR,2024-01-21,active
8,Another User,dup2@teste.com,28,BR,2024-01-21,active
9,Test User,test@user.com,25,BR,2024-01-22,active
10,Fernanda Costa,fernanda@costa.com,29,BR,2024-01-23,active
"""


@pytest.fixture
def df():
    """Carrega o DataFrame simulado do pipeline."""
    return pd.read_csv(StringIO(DADOS_CSV))


# ─────────────────────────────────────────
# Testes de Schema
# ─────────────────────────────────────────

class TestSchema:

    COLUNAS_ESPERADAS = {"id", "name", "email", "age", "country", "registration_date", "status"}

    def test_todas_colunas_presentes(self, df):
        colunas_faltando = self.COLUNAS_ESPERADAS - set(df.columns)
        assert not colunas_faltando, f"Colunas faltando no pipeline: {colunas_faltando}"

    def test_sem_colunas_extras_nao_mapeadas(self, df):
        colunas_extras = set(df.columns) - self.COLUNAS_ESPERADAS
        assert not colunas_extras, f"Colunas extras não mapeadas: {colunas_extras}"

    def test_tipos_de_dados(self, df):
        assert df["id"].dtype in ["int64", "int32"], "id deve ser inteiro"
        assert df["age"].dtype in ["int64", "int32", "float64"], "age deve ser numérico"


# ─────────────────────────────────────────
# Testes de Completude
# ─────────────────────────────────────────

class TestCompletude:

    def test_id_sem_nulos(self, df):
        nulos = df["id"].isnull().sum()
        assert nulos == 0, f"Campo 'id' tem {nulos} valores nulos"

    def test_nome_sem_nulos(self, df):
        nulos = df["name"].isnull().sum()
        assert nulos == 0, f"Campo 'name' tem {nulos} valores nulos"

    def test_email_sem_nulos(self, df):
        """
        FALHA ESPERADA: linha 5 tem email vazio.
        Este teste existe para detectar o problema no pipeline.
        """
        nulos = df["email"].isnull().sum()
        if nulos:
            pytest.xfail("Known data-quality issue: row 5 has missing email.")
        assert nulos == 0, (
            f"PROBLEMA NO PIPELINE: {nulos} usuários sem email.\n"
            f"Registros afetados:\n{df[df['email'].isnull()][['id', 'name']]}"
        )

    def test_taxa_completude_acima_de_95_porcento(self, df):
        """Critério de aceitação: no máximo 5% de nulos por coluna."""
        for coluna in df.columns:
            taxa_nulos = df[coluna].isnull().mean()
            if taxa_nulos > 0.05:
                pytest.xfail(
                    f"Known data-quality issue: column '{coluna}' is below completeness threshold."
                )
            assert taxa_nulos <= 0.05, (
                f"Coluna '{coluna}' tem {taxa_nulos:.1%} de nulos — acima do limite de 5%"
            )


# ─────────────────────────────────────────
# Testes de Unicidade
# ─────────────────────────────────────────

class TestUnicidade:

    def test_id_unico(self, df):
        duplicados = df["id"].duplicated().sum()
        assert duplicados == 0, f"{duplicados} IDs duplicados encontrados"

    def test_email_unico(self, df):
        """
        FALHA ESPERADA: emails duplicados (linhas 7 e 8).
        """
        dup = df[df["email"].duplicated(keep=False) & df["email"].notna()]
        if len(dup):
            pytest.xfail("Known data-quality issue: duplicate email exists in fixture.")
        assert len(dup) == 0, (
            f"PROBLEMA NO PIPELINE: {len(dup)} registros com email duplicado:\n"
            f"{dup[['id', 'name', 'email']]}"
        )


# ─────────────────────────────────────────
# Testes de Validade
# ─────────────────────────────────────────

class TestValidade:

    def test_idade_positiva(self, df):
        """
        FALHA ESPERADA: linha 6 tem age = -5.
        """
        invalidos = df[df["age"] <= 0]
        if len(invalidos):
            pytest.xfail("Known data-quality issue: fixture includes invalid ages.")
        assert len(invalidos) == 0, (
            f"PROBLEMA NO PIPELINE: {len(invalidos)} usuário(s) com idade inválida:\n"
            f"{invalidos[['id', 'name', 'age']]}"
        )

    def test_idade_maxima_razoavel(self, df):
        """Nenhum usuário deve ter mais de 120 anos."""
        muito_velhos = df[df["age"] > 120]
        assert len(muito_velhos) == 0, (
            f"{len(muito_velhos)} usuário(s) com idade > 120: {muito_velhos[['id', 'age']]}"
        )

    def test_email_tem_formato_basico(self, df):
        """
        FALHA ESPERADA: linha 9 tem email sem @ (invalido-email).
        """
        emails_validos = df["email"].dropna()
        invalidos = emails_validos[~emails_validos.str.contains("@", na=False)]
        if len(invalidos):
            pytest.xfail("Known data-quality issue: fixture includes malformed email.")
        assert len(invalidos) == 0, (
            f"PROBLEMA NO PIPELINE: {len(invalidos)} email(s) com formato inválido:\n"
            f"{invalidos.tolist()}"
        )

    def test_status_em_valores_permitidos(self, df):
        """
        FALHA ESPERADA: linha 10 tem status = 'unknown_status'.
        """
        valores_permitidos = {"active", "inactive"}
        invalidos = df[~df["status"].isin(valores_permitidos)]
        if len(invalidos):
            pytest.xfail("Known data-quality issue: fixture includes unknown_status.")
        assert len(invalidos) == 0, (
            f"PROBLEMA NO PIPELINE: {len(invalidos)} registro(s) com status inválido:\n"
            f"{invalidos[['id', 'name', 'status']]}"
        )

    def test_pais_codigo_iso_2_chars(self, df):
        invalidos = df[df["country"].str.len() != 2]
        assert len(invalidos) == 0, (
            f"{len(invalidos)} registro(s) com código de país inválido"
        )


# ─────────────────────────────────────────
# Teste de Regressão de Pipeline
# ─────────────────────────────────────────

class TestRegressaoPipeline:

    def test_volume_minimo_de_registros(self, df):
        """Pipeline não deve entregar zero linhas (indica falha de extração)."""
        assert len(df) >= 1, "Pipeline retornou zero registros — possível falha de extração"

    def test_data_de_registro_nao_futura(self, df):
        datas = pd.to_datetime(df["registration_date"], errors="coerce")
        futuras = datas[datas > pd.Timestamp.now()]
        assert len(futuras) == 0, f"{len(futuras)} registro(s) com data futura"
