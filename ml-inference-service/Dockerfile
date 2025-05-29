FROM python:3.9-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages && \
    rm -rf /var/lib/apt/lists/*

COPY . .

ENV PORT 8080
EXPOSE $PORT

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]