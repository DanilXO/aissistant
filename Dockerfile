FROM python:3.10-slim-buster

RUN apt-get update && apt-get -y upgrade  \
    && apt-get install -y build-essential  \
    libssl-dev  \
    libffi-dev  \
    python3-dev  \
    libasound-dev  \
    libportaudio2  \
    libportaudiocpp0  \
    portaudio19-dev  \
    flac  \
    python-pyaudio  \
    pulseaudio  \
    pulseaudio-utils

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.1

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY . /app

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

ENTRYPOINT ["poetry", "run", "python", "-m", "src.demo"]