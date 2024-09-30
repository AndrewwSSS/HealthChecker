FROM python:3.11.9-alpine3.19
LABEL maintainer="clash2clans1one@gmail.com"

RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT ["sh", "entrypoint.sh"]