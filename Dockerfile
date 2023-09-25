FROM python:3.11-alpine

RUN mkdir /src

COPY . /src

RUN cd /src && pip install .

WORKDIR /workdir

ENTRYPOINT [ "bibtefmt" ]
