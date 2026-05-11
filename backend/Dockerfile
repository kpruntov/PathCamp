FROM python:3.11-slim as builder
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml README.md ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi
COPY app app

FROM gcr.io/distroless/python3-debian12
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages
CMD ["-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
