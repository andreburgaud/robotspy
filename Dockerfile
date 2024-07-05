FROM python:3.9.2-alpine3.13

ENV     ROBOTSPY_VERSION=0.8.0 \
        maintainer="andre.burgaud@gmail.com"

LABEL   robotspy.version=$ROBOTSPY_VERSION
LABEL   python.version=$PYTHON_VERSION

RUN     pip install --no-cache-dir --upgrade pip && \
        pip install --no-cache-dir robotspy==$ROBOTSPY_VERSION

ENTRYPOINT ["robots"]

CMD ["--help"]