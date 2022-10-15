FROM python:3.8.5-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
RUN mkdir /app/logs
RUN mkdir /app/tmp
WORKDIR /app

RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base
RUN apk add gcc libffi-dev musl-dev \
    tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
    libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
    libxcb-dev libpng-dev
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip3 install -r requirements.txt

COPY . /app