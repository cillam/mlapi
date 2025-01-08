# Dockerfile
## Build venv stage
FROM python:3.11-slim AS builder

### Install curl
RUN apt-get update \
    && apt-get install -y \
         curl \
         build-essential \
         libffi-dev \
    && rm -rf /var/lib/apt/lists/*

### Install poetry
RUN  curl -sSL https://install.python-poetry.org | python3 -

### Set up poetry
ENV PATH=/root/.local/bin:${PATH}

### Set working directory
WORKDIR /app

### Copy poetry.lock and pyproject.toml
COPY pyproject.toml poetry.lock ./

### Install dependencies
RUN python -m venv --copies /app/venv
RUN . /app/venv/bin/activate && poetry install --only main


## Runtime stage
### Get python
FROM python:3.11-slim AS runner

### Set up venv
COPY --from=builder /app/venv /app/venv/
ENV PATH=/app/venv/bin:${PATH}

WORKDIR /app

# Copy our source code
COPY . .

# Run application
CMD uvicorn src.main:app --host 0.0.0.0 --port 8000
