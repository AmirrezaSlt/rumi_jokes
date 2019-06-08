FROM python:3
ENV PYTHONPATH /usr/bin/python3
ENV FLASK_DEBUG 1
ENV FLASK_APP /code/run.py
ENV PORT 5000

COPY ./rumi_project ./code
WORKDIR /code
RUN pip install -r ./rumi_jokes/requirements.txt

CMD flask run -h 0.0.0.0 -p 5000
