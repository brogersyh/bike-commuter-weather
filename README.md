# bike-commuter-weather

The Python-REST-Service is the service-backend for a Bike Commuter Weather App intended for bicycle commuters, for whom wind speed and direction are critical parameters - many weather apps leave this out or de-emphasize it.

Built Image(s) (both Linux and Windows images) for the below available at [DockerHub/brogersyh](https://hub.docker.com/r/brogersyh/)

* docker build -t bcwservice ./Python-REST-Service

  * docker run -d -e WUNDERGROUND_API_KEY=YourWundergroundApiKey -p 5000:5000 bcwservice
