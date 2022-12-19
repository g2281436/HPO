FROM ubuntu:22.04

ENV PYTHONUNBUFFERED=TRUE \
    PYTHONDONTWRITEBYTECODE=TRUE \
    TZ="Asia/Tokyo" \
    LANG=ja_JP.UTF-8 \
    LANGUAGE=ja_JP:en \
    PATH=$PATH:/opt/conda/bin \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /opt

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        wget \
        git \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get purge --auto-remove && \
    apt-get clean

WORKDIR /usr/local/src

ARG ANACONDA3_VERSION=2022.10
ARG PYTHON_VERSION=3.9

RUN wget -q https://repo.continuum.io/archive/Anaconda3-${ANACONDA3_VERSION}-Linux-x86_64.sh -P ./downloads/ && \
    bash ./downloads/Anaconda3-${ANACONDA3_VERSION}-Linux-x86_64.sh -b -p /opt/conda && \
    rm -rf ./downloads

RUN git clone https://github.com/aistairc/aiaccel.git

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -rf requirements.txt aiaccel

RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        locales \
        apt-utils && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get purge --auto-remove && \
    apt-get clean

RUN cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    locale-gen ja_JP.UTF-8

ENV TZ="Asia/Tokyo" \
    LANG=ja_JP.UTF-8 \
    LANGUAGE=ja_JP:en \
    PYTHONPATH=/opt/ml/src 

COPY . /work

RUN useradd signate -m -u 1000
RUN chown -R signate:signate /work

WORKDIR /work

USER signate
