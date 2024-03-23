FROM python:3.12

WORKDIR /app

COPY requirements.in /app/requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Install ffmeg
RUN apt-get update
RUN apt-get install -y ffmpeg

COPY . /app

EXPOSE 8000