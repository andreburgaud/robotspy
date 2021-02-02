FROM python:3.9.1-alpine3.12

ENV     ROBOTSPY_VERSION=0.5.1 \
        maintainer="andre.burgaud@gmail.com"

LABEL   robotspy.version=$ROBOTSPY_VERSION
LABEL   python.version=$PYTHON_VERSION

RUN     pip install --no-cache-dir --upgrade pip && \
        pip install --no-cache-dir robotspy==$ROBOTSPY_VERSION

ENTRYPOINT ["robots"]

CMD ["--help"]