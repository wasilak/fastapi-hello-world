FROM python:3-alpine

RUN apk add --update --no-cache build-base dumb-init

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY ./app /app/

WORKDIR /app

EXPOSE 5000

ENV SECRET_KEY=cne287fg8237hc38igochh98cy^TR^&%R&T*&G

ENV SESSION_COOKIE_NAME=session-fastapi-hello-world

ENTRYPOINT ["/usr/bin/dumb-init", "--", "uvicorn", "main:app", "--host=0.0.0.0", "--port=5000"]

CMD ["--reload", "--log-level=info"]
