FROM ubuntu:18.04

ENV WORK_DIR=/app
ENV PYTHONUNBUFFERED=true
ENV LC_ALL=C.UTF-8

WORKDIR $WORK_DIR

# Install Python2 & Python3
RUN DEBIAN_FRONTEND=noninteractive apt-get -y update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y dist-upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential wget tar \
        python python-pip python-wheel python-setuptools \
        python3 python3-pip python3-wheel python3-setuptools


# Install Python dependencies
COPY requirements.txt $WORK_DIR
COPY requirements-dev.txt $WORK_DIR
RUN python -m pip install --trusted-host mirrors.cloud.tencent.com \
    -i http://mirrors.cloud.tencent.com/pypi/simple/ -r requirements-dev.txt
RUN python3 -m pip install --trusted-host mirrors.cloud.tencent.com \
    -i http://mirrors.cloud.tencent.com/pypi/simple/ -r requirements-dev.txt

# Install source files
COPY . $WORK_DIR
RUN python -m pip install .
RUN python3 -m pip install .
