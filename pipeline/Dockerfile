FROM python:3.13.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code
COPY pyproject.toml README.md .python-version uv.lock ./
COPY src ./src
RUN uv sync --locked
COPY pipeline.py .

ENTRYPOINT ["uv" , "run",  "python", "pipeline.py"]

