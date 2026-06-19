FROM python:3.11-slim

WORKDIR /app

# Copy requirements from the build context root. When building with
# `docker build -f demo_app/Dockerfile .` the repo root is the build context
# and `requirements.txt` is available at the path below.
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the demo_app sources into the image
COPY . /app

EXPOSE 3000

CMD ["uvicorn", "demo_app.main:app", "--host", "0.0.0.0", "--port", "3000"]
