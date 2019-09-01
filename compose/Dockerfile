FROM ubuntu:16.04

ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"

ENV TZ=Asia/Seoul

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean \
    && apt-get install -y \
        chromium-browser \
        tzdata \
        python3-pip \
        build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

COPY ./robot.py /app/robot.py
COPY ./settings.py /app/settings.py
COPY ./slack.py /app/slack.py
COPY ./functions /app/functions
COPY ./compose/start /start

RUN chmod +x /start \
    && chmod +x /app/functions/utils/chromedriver/chromedriver \
    && mkdir -p /var/www/html/screenshots
 
WORKDIR /app

ENTRYPOINT /start
