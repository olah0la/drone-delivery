FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY generate_events.py .

CMD ["python", "generate_events.py", "${BASE_URL}"]
