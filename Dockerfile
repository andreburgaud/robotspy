# syntax=docker/dockerfile:1

FROM python:3.13.5-alpine3.22

ENV     ROBOTSPY_VERSION=0.12.0 \
        maintainer="andre.burgaud@gmail.com" \
        ROBOTSUSER="robotsuser" \
        ROBOTSGROUP="robotsgroup"

LABEL   robotspy.version=$ROBOTSPY_VERSION
LABEL   python.version=$PYTHON_VERSION

RUN addgroup -S $ROBOTSGROUP
RUN adduser -S -G $ROBOTSGROUP $ROBOTSUSER
USER $ROBOTSUSER

ENV PATH="/home/$ROBOTSUSER/.local/bin:$PATH"

RUN     pip install --no-cache-dir --upgrade pip && \
        pip install --no-cache-dir robotspy==$ROBOTSPY_VERSION

ENTRYPOINT ["robots"]

CMD ["--help"]