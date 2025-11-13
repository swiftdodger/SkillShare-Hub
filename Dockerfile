FROM ubuntu:latest
LABEL authors="flavio-gabriel"

ENTRYPOINT ["top", "-b"]