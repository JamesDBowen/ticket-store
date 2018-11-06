FROM ubuntu:18.04

EXPOSE 8000

RUN apt-get update --fix-missing && apt-get upgrade -y
RUN apt-get install -y build-essential
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-dev


WORKDIR /app

ADD ./requirements.txt /app/requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./ /app

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
