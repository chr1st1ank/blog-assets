FROM node:24-bookworm-slim@sha256:d6aa754f16b3197301076f047b5def2f02ea1dbbc2ca920407d46d7ec7f87b20 AS node
FROM ghcr.io/astral-sh/uv:0.12.19@sha256:04d046b13e60d6bcec73cbc5e1cad25d680dea90c8573340950a0ac2d1aef424 AS uv
FROM python:3.14-slim-bookworm@sha256:48b13b003dda20b16f9442b8475aa05fe21bf6579a8c881db92ffb4d8fd20f83

COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
COPY --from=uv /uv /usr/local/bin/uv
COPY --from=host-tools task /usr/local/bin/task
COPY --from=host-tools gh /usr/local/bin/gh
RUN ln -s ../lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
    && apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl git podman crun uidmap fuse-overlayfs slirp4netns \
    && rm -rf /var/lib/apt/lists/* \
    && npm install --global --allow-scripts=@opencode/cli @opencode/cli@2.0.23 \
    && npm cache clean --force \
    && uv pip install --system --no-cache --exclude-newer 2026-10-06 podman-compose==1.6.0
COPY containers.conf /etc/containers/containers.conf
ENV UV_PROJECT_ENVIRONMENT=/opt/poc-venv \
    UV_SYSTEM_CERTS=true \
    NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
WORKDIR /workspace
CMD ["sh"]
