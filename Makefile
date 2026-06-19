.PHONY: app test test-api test-ui test-data test-llm install-browsers

app:
	uvicorn demo_app.main:app --host 127.0.0.1 --port 3000 --reload

install-browsers:
	playwright install chromium

test:
	pytest -v -m "not requires_openai"

test-api:
	pytest api-tests/ -v

test-ui:
	pytest automation/ui/ -v

test-data:
	pytest data-quality/ -v

test-llm:
	pytest llm-tests/eval/ -v -m requires_openai
