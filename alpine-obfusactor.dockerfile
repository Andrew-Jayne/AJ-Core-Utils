# === Stage 1: Build and obfuscate ===
FROM python:3.13-alpine AS builder

ENV PYTHONUNBUFFERED=1
ARG APP_USER=appuser
ARG APP_UID=1001
ARG APP_GROUP=appgroup
ARG APP_GID=1001
ARG MAIN_SCRIPT=main.py

# Install only essential build tools
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev

# Create non-root user
RUN addgroup -g ${APP_GID} ${APP_GROUP} && \
    adduser -D -u ${APP_UID} -G ${APP_GROUP} ${APP_USER}

# Install pyarmor
RUN pip install --no-cache-dir pyarmor

# Set working dir and switch to non-root user
WORKDIR /build
RUN chown ${APP_USER}:${APP_GROUP} /build
USER ${APP_USER}

# Install Python dependencies
COPY --chown=${APP_USER}:${APP_GROUP} requirements.txt ./
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy the source code
COPY --chown=${APP_USER}:${APP_GROUP} . .

# Obfuscate the code
RUN pyarmor gen -O dist ${MAIN_SCRIPT}

# === Stage 2: Minimal runtime with obfuscated code ===
FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1
ARG APP_USER=appuser
ARG APP_UID=1001
ARG APP_GROUP=appgroup
ARG APP_GID=1001

# Create runtime user
RUN addgroup -g ${APP_GID} ${APP_GROUP} && \
    adduser -D -u ${APP_UID} -G ${APP_GROUP} ${APP_USER}

# Set working directory
WORKDIR /app
RUN chown ${APP_USER}:${APP_GROUP} /app
USER ${APP_USER}

# Copy installed Python packages
COPY --from=builder --chown=${APP_USER}:${APP_GROUP} /home/${APP_USER}/.local /home/${APP_USER}/.local
ENV PATH="/home/${APP_USER}/.local/bin:$PATH"

# Copy obfuscated code
COPY --from=builder --chown=${APP_USER}:${APP_GROUP} /build/dist /app

# Run the obfuscated app
CMD ["python3", "main.py"]
