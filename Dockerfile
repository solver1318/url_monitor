FROM python:3.7-slim

WORKDIR /app

COPY src/ .
COPY requirements.txt .

# Install pip requirements
RUN pip install -r requirements.txt
