FROM python:3.8-slim-buster
WORKDIR /usr/app/src

COPY generate_daemon_set.py ./

# RUN apt-get update && apt-get upgrade -y
RUN python -m pip install --upgrade setuptools && pip install requests

ENTRYPOINT [ "python", "./generate_daemon_set.py"]
