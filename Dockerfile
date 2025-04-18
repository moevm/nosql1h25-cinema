FROM python:3.13-alpine

WORKDIR /app

ENV FLASK_APP=app/run.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "run"]
