FROM python:3.10

# set lang
ENV LANG C.UTF-8

# Set the working directory to /app
WORKDIR /app

COPY requirements.txt /app

RUN apt-get update

# install
RUN pip install -r requirements.txt

COPY . /app

RUN \
    rm -r .git \
    && rm .gitignore \
    && rm docker-compose.yml \
    && rm docker_build.sh \
    && rm Dockerfile \
    && rm -r models \
    && rm -r notebook \
    && rm -r stress

ENV TZ=America/Argentina/Buenos_Aires

CMD ["python", "api.py"]
