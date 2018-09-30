FROM python:3.6.6-alpine3.7

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONPATH=/code

RUN mkdir /code
COPY scripts/log_server.py /code
WORKDIR /code

ENTRYPOINT [ "python", "log_server.py" ]
