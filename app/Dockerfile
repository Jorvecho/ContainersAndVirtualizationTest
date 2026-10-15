FROM python:3.13.2-slim

RUN useradd -m -u 1000 appuser

COPY ./ ./

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
