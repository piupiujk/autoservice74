FROM python:3.14.2

RUN pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR /autoservice

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

# Копируем код
COPY . .

## Создаем пользователя
#RUN adduser --disabled-password --gecos '' appuser && \
#    chown -R appuser:appuser /app
#USER appuser

ENTRYPOINT ["./entrypoint.sh"]