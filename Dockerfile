FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev --no-install-project

COPY . .

EXPOSE 80

CMD ["uv", "run", "uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "80"]
