FROM ubuntu:18.04

ENV PORT=${PORT}
ENV HOST=${HOST}

ADD . /code
WORKDIR /code

RUN apt-get update -y \
    && apt-get install -y \
#    gunicorn \
    python3-dev \
    python3-pip

RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD ["python3", "app/app.py"]