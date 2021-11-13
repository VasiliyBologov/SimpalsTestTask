FROM python:3.9-slim-buster as Client-Portal

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# https://serverfault.com/questions/949991/how-to-install-tzdata-on-a-ubuntu-docker-image
ENV DEBIAN_FRONTEND noninteractive

# OS dependencies
RUN apt update && apt install --no-install-recommends --no-install-suggests -y \
    openssh-server \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    gcc \
    nginx \
    htop
RUN pip3 install poetry



WORKDIR /app


# Copy only requirements to cache them in the Docker layer
COPY ./poetry.lock ./
COPY ./pyproject.toml ./

# App dependencies. We don't need virtual environment in Docker
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-dev

# Copy app files
COPY ./ ./
COPY docker/site.conf ./
COPY docker/start.sh ./

# Nginx
RUN rm /etc/nginx/sites-enabled/* -f && ln -s /app/site.conf /etc/nginx/sites-enabled/

EXPOSE 80

RUN chmod +x ./start.sh
RUN chmod +x ./main.py

# Run
CMD ./start.sh
