FROM python:3.12-slim

WORKDIR /app

COPY Backend/requirements.txt .
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY Backend/ .

# Ambiente de Produção: usa Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:create_app()"]
