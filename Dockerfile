# Use the official uv image for optimized builds
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install the project into `/app`
WORKDIR /app

# Copy only dependency files to cache them
COPY pyproject.toml uv.lock ./

# Download dependencies (Docker will skip this if your lockfile hasn't changed)
RUN uv sync --frozen

# Copy the source code into the container.
COPY . .

# Place executables in the path
ENV PATH="/app/.venv/bin:$PATH"

# Expose the port that the application listens on.
EXPOSE 8001

# Run the application using uvicorn
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "4"]