FROM python:3.9
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY src /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
