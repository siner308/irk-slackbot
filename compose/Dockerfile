FROM ubuntu:18.04

ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"
ENV DEBIAN_FRONTEND="noninteractive"
ENV TZ="Asia/Seoul"

COPY ./google-chrome-stable_current_amd64.deb /google-chrome-stable_current_amd64.deb

RUN apt-get update && apt-get autoremove && apt-get autoclean \
    && apt-get install -y \
        tzdata \
        python3-pip \
        build-essential \
        libxss1 \
        libgconf2-4 \
        libappindicator1 \
        libindicator7 \
        fonts-liberation \
        libasound2 \
        libnspr4 \
        libnss3 \
        libx11-xcb1 \
        wget \
        xdg-utils \
        libappindicator3-1 \
        libatk-bridge2.0-0 \
        libatspi2.0-0 \
        libgtk-3-0 \
    && dpkg -i /google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/* \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

COPY ./robot.py /app/robot.py
COPY ./settings.py /app/settings.py
COPY ./logger.py /app/logger.py
COPY ./chromedriver.py /app/chromedriver.py
COPY ./chromedriver /app/chromedriver
COPY ./apps /app/apps
COPY ./compose/start /start

RUN chmod +x /start \
    && chmod +x /app/chromedriver \
    && mkdir -p /var/www/html/screenshots
 
WORKDIR /app

ENTRYPOINT /start
