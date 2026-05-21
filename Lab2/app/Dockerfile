FROM python:3.13-slim

WORKDIR /opt/mywebapp

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:app"]