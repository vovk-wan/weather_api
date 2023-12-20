FROM python:3.11.1-bullseye
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN apt-get update && \
    apt-get install -y locales && \
    apt-get install -y python-dev python3-dev libldap2-dev libsasl2-dev libssl-dev netcat-openbsd poppler-utils && \
    echo ru_RU.UTF-8 UTF-8 >> /etc/locale.gen && \
    locale-gen

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000