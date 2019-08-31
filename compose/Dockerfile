FROM python:3.5

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY ./robot.py /app/robot.py
COPY ./settings.py /app/settings.py
COPY ./slack.py /app/slack.py
COPY ./functions /app/functions
COPY ./compose/start /start

RUN chmod +x /start
 
WORKDIR /app

ENTRYPOINT /start
