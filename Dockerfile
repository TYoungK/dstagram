FROM python:3.8.5
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip3 install -r requirements.txt

COPY . /app/