# Dockerfile
# OpenEnv strictly recommends Python 3.10+
FROM python:3.11-slim

# Install git, curl, and any other system dependencies needed for pytest and uv
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

# Install uv (The recommended fast package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Create a non-root user for security (best practice for HF Spaces)
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /app

# Copy the modern dependency file
COPY pyproject.toml ./

# Install dependencies using uv directly into the system python for the container
# uv is smart enough to read the dependencies array directly from pyproject.toml!
RUN uv pip install --system -r pyproject.toml

# Copy the rest of the application files
COPY openenv.yaml README.md inference.py ./
COPY src/ ./src/
COPY server/ ./server/

# Change ownership to the non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Expose the standard Hugging Face port
EXPOSE 7860

# The standard entrypoint required by OpenEnv
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]