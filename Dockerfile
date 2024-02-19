FROM python:3.10-slim-buster as base
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.10-slim-buster
COPY --from=base . .
WORKDIR /app
COPY app/ ./app
ENV PORT=8000
EXPOSE ${PORT}

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]