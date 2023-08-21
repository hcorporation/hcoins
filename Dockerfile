FROM python:3.11
ENV POETRY_VERSION=1.5.1
RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /hcoins
COPY poetry.lock pyproject.toml /hcoins/
RUN poetry install --no-interaction --no-ansi
COPY . /hcoins/
CMD poetry run python3 index.py