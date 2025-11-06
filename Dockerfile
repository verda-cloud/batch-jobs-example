FROM ghcr.io/astral-sh/uv:python3.13-alpine

# Override inherited labels
LABEL org.opencontainers.image.description="A simple example app for containers batch jobs"
LABEL org.opencontainers.image.source="https://github.com/verda-cloud/batch-jobs-example"
LABEL org.opencontainers.image.title="Batch Jobs Example"

# PYTHONDONTWRITEBYTECODE=1: disable .pyc bytecode files to keep layers clean
# PYTHONUNBUFFERED=1: unbuffer stdout/stderr so logs flush immediately
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy project files first to leverage Docker layer caching for deps
COPY pyproject.toml uv.lock ./

# Install dependencies with uv into a project venv (.venv)
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev

# Ensure venv is used by default
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY main.py /app/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]


