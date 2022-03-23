FROM docker.causeex.com/dart/centos-python3:latest

LABEL maintainer="yan.zverev@twosixlabs.com, michael.reynolds@twosixlabs.com, nicholas.sanchirico@twosixlabs.com"

RUN yum -y update
RUN yum -y install zip && \
    yum -y install vim && \
    yum -y install openssl && \
    yum clean all && \
    rm -r -f /var/cache/yum

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
