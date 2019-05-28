FROM python:3
COPY ./rumi_project ./code
WORKDIR /code
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "run.py" ]
