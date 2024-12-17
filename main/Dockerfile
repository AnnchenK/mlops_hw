FROM python:3.13
COPY run.sh ./run.sh
COPY pyproject.toml ./pyproject.toml
RUN sed -i 's/\r$//' ./run.sh
RUN pip install -U poetry
RUN poetry install
ENTRYPOINT ["bash", "./run.sh"]