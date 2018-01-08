FROM ubuntu:latest

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  nodejs \
  npm \
  nodejs-legacy \
  python \
  python-setuptools \
  python-pip \
  python-dev \
  build-essential \
  git \
  cron \
  vim\
  libpq-dev \
  lib32ncurses5-dev \
  libgeos-dev

RUN mkdir webhook

ADD dashboard webhook

WORKDIR webhook

RUN pip install -r requirements.txt
EXPOSE 8000

CMD ["./start.sh"]
