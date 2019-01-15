FROM python:3.6-jessie
ENV DOCKERIZE_VERSION v0.3.0
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt