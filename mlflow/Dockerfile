FROM python:3.9.13-slim

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install -U mlflow

COPY run.sh ./run.sh
RUN sed -i 's/\r$//' ./run.sh
ENTRYPOINT ["bash", "./run.sh"]