#
FROM python:3.6.5-slim

MAINTAINER Aoi.Kuiyuyou <aoi.kuiyuyou@gmail.com>

COPY ./aoikconsulwatcher /opt/aoikconsulwatcherhosts/aoikconsulwatcher

RUN pip install -r \
    /opt/aoikconsulwatcherhosts/aoikconsulwatcher/requirements.txt

COPY ./dumb-init/1.2.1/bin/dumb-init_1.2.1_amd64 /sbin/dumb-init

RUN chmod 755 /sbin/dumb-init

RUN rm -rf /root/.cache && \
    rm -rf /tmp/*

WORKDIR /

CMD [ \
    "/sbin/dumb-init", \
    "python", \
    "/opt/aoikconsulwatcherhosts/aoikconsulwatcher/src/aoikconsulwatcher/__main__.py", \
    "--config", \
    "/opt/aoikconsulwatcherhosts/aoikconsulwatcher/conf/config.py" \
]
