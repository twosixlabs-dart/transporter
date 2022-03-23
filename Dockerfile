FROM python:3.9

LABEL maintainer="yan.zverev@twosixlabs.com, michael.reynolds@twosixlabs.com, nicholas.sanchirico@twosixlabs.com"

RUN apt-get update
RUN apt-get -y install zip vim openssl && \
    apt-get clean all

ENV PYTHONUNBUFFERED true
ENV LADLE_HOST "localhost"
ENV LADLE_PORT 8080
ENV SOURCE_DIR "/opt/app/data/inbound"
ENV TARGET_DIR "/opt/app/data/completed"

RUN mkdir -p $SOURCE_DIR
RUN mkdir -p $TARGET_DIR

ADD . /opt/app/
WORKDIR /opt/app
RUN python3 setup.py install

ENTRYPOINT transporter --source $SOURCE_DIR --target $TARGET_DIR --patterns raw --host ladle --port 8080
