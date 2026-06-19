# QA Portfolio - Automacao, Dados & IA

> Projeto de portfólio demonstrando testes em sistemas web, APIs REST, pipelines de dados e modelos de linguagem (LLMs).  
> Cobre desde QA clássico até **AI Quality Engineering** — posição de alta demanda no mercado internacional.

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
├── data-quality/            # Validação de dados com Great Expectations
│   └── test_data_pipeline.py
│
├── llm-tests/               # AI Quality Engineering
│   ├── eval/
│   │   └── test_llm_hallucination.py
│   ├── prompts/
│   │   └── adversarial_prompts.md
│   └── reports/
│       └── llm_quality_report.md
│
└── .github/
    └── workflows/
        └── ci.yml
```

---

## 🚀 Quick Start

```bash
# Clone o projeto
git clone https://github.com/seu-usuario/llm-qa-portfolio.git
cd llm-qa-portfolio

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt

# Instale o Playwright
playwright install chromium

# Execute todos os testes
pytest --html=report.html --self-contained-html
```

---

## 🧩 Stack Tecnológica

| Camada | Ferramenta | Por quê |
|--------|-----------|---------|
| UI Automation | Playwright + Pytest | Padrão moderno do mercado |
| API Testing | Requests + Pytest | Flexível e fácil de integrar no CI |
| Data Quality | Great Expectations | Usado em pipelines de produção |
| LLM Evaluation | OpenAI SDK + custom | Sem framework que trave o raciocínio |
| CI/CD | GitHub Actions | Portfólio visível para recrutadores |
| Reports | pytest-html | Saída profissional para apresentar |

---

## 🧠 Módulo LLM Tests — Destaque do Portfólio

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
Login UI             8         100%
API Users            12        100%
Data Pipeline        6         85%
LLM Evaluation       15        —  (qualitative)
─────────────────────────────────────────
Total                41
```

---

## 📄 Licença

MIT — fique à vontade para usar como base do seu próprio portfólio.
