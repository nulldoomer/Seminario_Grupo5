FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

RUN pip install uv

# Copy dependency files
COPY pyproject.toml .
COPY uv.lock .

# Install dependencies
RUN uv sync --frozen

COPY . .

RUN uv run scripts/pipeline/main.py

EXPOSE 8000

ENV PYTHONUNBUFFFERED=1

CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]