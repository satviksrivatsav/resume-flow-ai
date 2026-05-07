# syntax=docker/dockerfile:1

# Use the official uv image for optimized builds
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a container
ENV UV_LINK_MODE=copy

# Download dependencies as a separate step to take advantage of Docker's caching.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy the source code into the container.
COPY . .

# Install the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Place executables in the path
ENV PATH="/app/.venv/bin:$PATH"

# Create a non-privileged user that the app will run under.
RUN adduser --disabled-password --gecos "" --home "/nonexistent" --shell "/sbin/nologin" --no-create-home --uid 10001 appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application using uvicorn
# We use --host 0.0.0.0 to make it accessible outside the container
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
