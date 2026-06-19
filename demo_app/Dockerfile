FROM python:3.11-slim

WORKDIR /app

COPY ../requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 3000

CMD ["uvicorn", "demo_app.main:app", "--host", "0.0.0.0", "--port", "3000"]
