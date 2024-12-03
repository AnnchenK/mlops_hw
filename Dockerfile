FROM python:3.13
COPY run.sh ./run.sh
RUN sed -i 's/\r$//' ./run.sh
RUN pip install -U poetry
RUN pip install dvc[s3]
ENTRYPOINT ["bash", "./run.sh"]