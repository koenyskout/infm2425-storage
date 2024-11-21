FROM python:3.11-slim

WORKDIR /app

RUN pip install numpy paho-mqtt

COPY generator.py /app

CMD ["python", "generator.py"]
