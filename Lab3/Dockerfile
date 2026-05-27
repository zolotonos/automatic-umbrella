FROM python:3.10-slim
WORKDIR /opt/mywebapp
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .
RUN useradd -r -s /bin/false app && chown -R app:app /opt/mywebapp
USER app
ENTRYPOINT ["python", "start.py"]