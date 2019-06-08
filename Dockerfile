FROM python:3
COPY ./rumi_project ./code
WORKDIR /code
RUN pip install -r ./rumi_jokes/requirements.txt
CMD [ "python", "run.py" ]
