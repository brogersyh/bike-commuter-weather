# Dockerfiles-for-Linux

The Python-REST-Service is the service-backend for a Bike Commuter Weather App intended for bicycle commuters, for whom wind speed and direction are critical parameters - many weather apps leave this out or de-emphasize it.

* docker build -t Python-REST-Service ./Python-REST-Service
  * docker run -d -p 5000:5000 Python-REST-Service
