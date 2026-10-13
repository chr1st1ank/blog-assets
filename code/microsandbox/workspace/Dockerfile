FROM ghcr.io/astral-sh/uv:0.12.19@sha256:04d046b13e60d6bcec73cbc5e1cad25d680dea90c8573340950a0ac2d1aef424 AS uv

FROM python:3.14-slim-bookworm@sha256:48b13b003dda20b16f9442b8475aa05fe21bf6579a8c881db92ffb4d8fd20f83 AS build
COPY --from=uv /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=secret,id=msb_ca \
    if [ -f /run/secrets/msb_ca ]; then export SSL_CERT_FILE=/run/secrets/msb_ca UV_SYSTEM_CERTS=true; fi; \
    uv sync --locked --no-dev --no-editable
COPY hello_app ./hello_app

FROM python:3.14-slim-bookworm@sha256:48b13b003dda20b16f9442b8475aa05fe21bf6579a8c881db92ffb4d8fd20f83
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=build --chown=1000:1000 /app /app
USER 1000:1000
EXPOSE 8000
CMD ["uvicorn", "hello_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
