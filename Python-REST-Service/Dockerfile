FROM ubuntu:14.04

ENV WUNDERGROUND_API_KEY

# install python3
RUN apt-get update \
  && apt-get install -y --force-yes python python-dev python-setuptools software-properties-common gcc python-pip
  && apt-get clean all

# install python libraries
RUN pip install requests \
  && pip install Flask \
  && pip install python-dateutil

# copy working-dir-context files to image
ADD . /app

# Flask Port
EXPOSE 5000

ENTRYPOINT ["python","/app/public-service.py"]
