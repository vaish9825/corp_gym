# CORP-ENV — OpenEnv / Hugging Face Space (Python 3.11+)
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends git curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Tell uv sync to install into the system Python (no venv in Docker)
ENV UV_PROJECT_ENVIRONMENT="/usr/local"

COPY pyproject.toml uv.lock ./
COPY corp_env ./corp_env/
COPY server ./server/
COPY client ./client/
COPY data ./data/
COPY scripts ./scripts/
COPY training ./training/
COPY openenv.yaml README.md inference.py eval.py plot_results.py ./

RUN uv sync --frozen

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
