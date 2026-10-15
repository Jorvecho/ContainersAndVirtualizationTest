FROM python:3.13.2-slim

WORKDIR /app

COPY /api ./

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
