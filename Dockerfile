FROM python:3.6-buster


RUN apt-get update
RUN apt-get install -y libnotify-bin

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "bash", "./cowinscraper.sh" ]