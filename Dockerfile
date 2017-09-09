FROM python:2-slim

MAINTAINER Gary Reynolds <gary@touch.asn.au>

ARG PIP_EXTRA_ARGS

RUN apt-get update && apt-get -y install libzbar0 && apt-get clean
RUN pip install --no-cache-dir $PIP_EXTRA_ARGS pillow zbar
