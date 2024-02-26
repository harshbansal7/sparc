FROM python:3.12.1-slim-bookworm

WORKDIR /app

COPY requirements.txt .


RUN apt-get update && \
    apt-get install -y postgresql && \
    apt-get install -y libpq-dev gcc && \
    pip install --no-cache-dir -r requirements.txt

RUN spacy download en

COPY . .

EXPOSE 5001

CMD ["python", "app.py"]
