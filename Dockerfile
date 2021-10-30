FROM python:3.10

RUN mkdir /src

COPY . /src

RUN cd /src && pip install .

WORKDIR /workdir

ENTRYPOINT [ "bibtefmt" ]
