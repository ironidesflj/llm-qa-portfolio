# Ironides Junior - Portfolio QA, AI/ML QA & LLM Testing

[![QA Pipeline](https://github.com/ironidesflj/llm-qa-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/ironidesflj/llm-qa-portfolio/actions/workflows/ci.yml)

> Portfólio pessoal de testes para web, APIs REST, pipelines de dados e modelos de linguagem (LLMs).  
> Parte do meu roadmap para me tornar **AI/ML QA, LLM Testing e AI Quality Engineer**.

---

## 📁 Estrutura do Repositório

```
llm-qa-portfolio/
│
├── test-cases/              # Casos de teste manuais
│   └── TC-001_login.md
│
├── bug-reports/             # Bug reports documentados
│   └── BUG-001_login_bypass.md
│
├── api-tests/               # Testes de API em Python
│   └── test_api_users.py
│
├── automation/ui/           # Testes automatizados de UI
│   └── test_login_playwright.py
│
├── demo_app/                # App local usado pelos testes API/UI
│   └── main.py
│
├── data-quality/            # Validação de dados com Great Expectations
│   └── test_data_pipeline.py
│
├── llm-tests/               # AI Quality Engineering
│   ├── eval/
│   │   └── test_llm_hallucination.py
│   └── prompts/
│       └── adversarial_prompts.md
│
└── .github/
    └── workflows/
        └── ci.yml
```

---

## 🚀 Início Rápido

```bash
# Clone o projeto
git clone https://github.com/ironidesflj/llm-qa-portfolio.git
cd llm-qa-portfolio

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt

# Instale o Playwright
playwright install chromium

# Em um terminal, suba a app demo
make app

# Em outro terminal, execute a suite sem chamadas pagas de LLM
make test
```

### Notas sobre CI

- **Jobs de CI**: O pipeline executa múltiplos workflows: `ci.yml` (pipeline principal) e `api-tests.yml` (testes de API dedicados).
- **Demo App**: Os testes de API e UI rodam contra a aplicação FastAPI `demo_app` incluída na raiz do repositório.
- **Build Docker**: O `demo_app/Dockerfile` é construído com a raiz do repositório como contexto de build do Docker:
  - Localmente: `docker build -t llm-qa-portfolio-demo:latest -f demo_app/Dockerfile .`
  - Em CI: o workflow constrói com `-f demo_app/Dockerfile .` para acessar `requirements.txt` na raiz.
- **Playwright**: O job de automação UI instala bibliotecas de sistema requeridas no Ubuntu antes de instalar browsers do Playwright para evitar conflitos com `--with-deps`.
- **Avaliação de LLM**: Testes de LLM são pulados por padrão a menos que `OPENAI_API_KEY` seja configurada como um segredo do repositório no GitHub Actions.

#### Rodando a demo app localmente:
```bash
# Usando Make
make app

# Ou manualmente
python -m uvicorn demo_app.main:app --host 127.0.0.1 --port 3000
```

#### Construindo imagem Docker localmente:
```bash
docker build -t llm-qa-portfolio-demo:latest -f demo_app/Dockerfile .
docker run -d -p 3000:3000 llm-qa-portfolio-demo:latest
```

### Comandos úteis

```bash
make test-api      # testes de API contra a demo app
make test-ui       # testes de UI com Playwright
make test-data     # validações de qualidade de dados
make test-llm      # avaliação LLM real, requer OPENAI_API_KEY
```

---

## 📬 Contato

- LinkedIn: https://www.linkedin.com/in/ironjunior
- Email: ironidesflj@gmail.com

---

## 🧩 Stack Tecnológica

| Camada | Ferramenta | Por quê |
|--------|-----------|---------|
| UI Automation | Playwright + Pytest | Padrão moderno do mercado |
| API Testing | Requests + Pytest | Flexível e fácil de integrar no CI |
| Data Quality | Pandas + Pytest | Valida schema, completude, unicidade e regras de negócio |
| LLM Evaluation | OpenAI SDK + custom | Sem framework que trave o raciocínio |
| CI/CD | GitHub Actions | Portfólio visível para recrutadores |
| Reports | pytest-html | Saída profissional para apresentar |

---

## Destaques para Recrutadores

- Suite API/UI executável contra uma aplicação demo versionada no próprio repositório.
- Testes de dados documentam problemas reais com `xfail`, separando falhas conhecidas de regressões.
- Módulo LLM cobre alucinação, prompt injection, viés, consistência e formato de saída.

---

## 🧠 Módulo LLM Tests — Destaque do Portfólio (Testes de Modelos de Linguagem)

O módulo `llm-tests/` testa modelos de linguagem para:

- **Alucinações** — o modelo afirma fatos falsos com confiança?
- **Injeção de prompt** — o modelo ignora instruções do sistema?
- **Viés de resposta** — respostas mudam com perfis demográficos?
- **Consistência** — o modelo responde igual a perguntas paráfrases?
- **Toxicidade** — o modelo gera conteúdo prejudicial?

```python
# Exemplo de teste de alucinação
def test_model_should_not_hallucinate_capitals():
    response = ask_llm("Qual e a capital do Brasil?")
    assert "Brasilia" in response
    assert "São Paulo" not in response  # Erro comum de modelos
```

---

## 📊 Cobertura de Testes

```
Módulo               Testes    Cobertura
─────────────────────────────────────────
Login UI             9         100%
API Users            12        100%
Data Pipeline        16        10 pass / 6 known issues
LLM Evaluation       13        qualitative
─────────────────────────────────────────
Total                50
```

---

## 📄 Licença

MIT — fique à vontade para usar como base do seu próprio portfólio. Boa sorte na sua jornada como QA!
