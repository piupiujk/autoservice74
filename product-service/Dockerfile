FROM python:3.14.2

RUN pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR /autoservice

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
