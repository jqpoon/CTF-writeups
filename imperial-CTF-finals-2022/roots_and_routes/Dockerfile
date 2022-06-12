FROM python:3.8-alpine

COPY ./web/requirements.txt /routes_bad/requirements.txt

WORKDIR /routes_bad

RUN pip install -r requirements.txt
COPY ./web /routes_bad

ENTRYPOINT [ "python" ]
CMD [ "server.py" ]   