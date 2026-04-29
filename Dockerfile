# ---- Base image ----
FROM python:3.12-slim

# ---- Environment ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Workdir ----
WORKDIR /app

# ---- System deps (optional but safe) ----
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Install Python deps ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy application ----
COPY app/ ./app/

# ---- OpenShift-friendly port ----
EXPOSE 8080

# ---- Run app (ASGI correct) ----
CMD ["gunicorn", "app.main:app", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8080", \
     "--workers", "2"]