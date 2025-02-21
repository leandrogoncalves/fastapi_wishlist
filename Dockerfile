FROM python:3.10-slim

ENV PYTHONPATH=/app

WORKDIR /app

COPY app/ /app/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]