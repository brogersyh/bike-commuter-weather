#!flask/bin/python

# Bike Commuter Weather app - REST service

from flask import Flask, jsonify, request, make_response

import json
import sys
import logging
import requests
import os

wundergroundApiKey = os.environ['WUNDERGROUND_API_KEY']

httpSuccessCode = 200

wundergroundBaseUrl = "http://api.wunderground.com/api/"
wundergroundConditions = "/conditions/q/"
wundergroundHourly = "/hourly/q/"
wundergroundHistory = "/history/q/"
wundergroundPwsPrefix = "pws:"
wundergroundJsonSuffix = ".json"

app = Flask(__name__)

# stubbed data
amWeatherData = [
    {
        'time': '06:00',
        'temperatureF': 25,
        'windSpeedMph': 15,
        'windDirection' : 'SSW',
        'precipitation': 'Snow'
    },
    {
        'time': '07:00',
        'temperatureF': 27,
        'windSpeedMph': 13,
        'windDirection' : 'SSW',
        'precipitation': 'Snow'
    },
    {
        'time': '08:00',
        'temperatureF': 31,
        'windSpeedMph': 11,
        'windDirection' : 'SSW',
        'precipitation': 'WintryMix'
    }
]

pmWeatherData = [
    {
        'time': '16:00',
        'temperatureF': 35,
        'windSpeedMph': 7,
        'windDirection' : 'N',
        'precipitation': 'None'
    },
    {
        'time': '17:00',
        'temperatureF': 34,
        'windSpeedMph': 9,
        'windDirection' : 'N',
        'precipitation': 'Rain'
    },
    {
        'time': '18:00',
        'temperatureF': 33,
        'windSpeedMph': 12,
        'windDirection' : 'N',
        'precipitation': 'Sleet'
    }
]

returnJson = {
    'error' : '',
    'info' : {
      'asOf' : "Mar 1, 3:01pm",
      'tempStationLoc' : 'Chicago Bronzeville, Chicago, Illinois',
      'windStationLoc' : 'U.S. Cellular Field/Bridgeport, Chicago, Illinois'
    },
    'today' : {
        'to' : {
            'now' : {
                'tempF' : 1,
                'windSpeedMph' : 10,
                'windGustMph' : 12,
                'windDirection' : 'N',
                'precipInHr' : 0.1,
                'humidityPct' : 50,
                'conditions' : 'clear'
            },
            'midpoint' : {
                'tempF' : 2,
                'windSpeedMph' : 11,
                'windGustMph' : 12,
                'windDirection' : 'NNE',
                'precipInHr' : 0,
                'humidityPct' : 50,
                'conditions' : 'cloudy'
            }
        },
        'from' : {
            'before' : {
                'tempF' : 3,
                'windSpeedMph' : 12,
                'windGustMph' : 12,
                'windDirection' : 'NE',
                'precipInHr' : 0.5,
                'humidityPct' : 50,
                'conditions' : 'rain'
            },
            'midpoint' : {
                'tempF' : 4,
                'windSpeedMph' : 13,
                'windGustMph' : 14,
                'windDirection' : 'E',
                'precipInHr' : 0.2,
                'humidityPct' : 50,
                'conditions' : 'snow'
            }
        }
    },
    'tomorrow' : {
        'to' : {
            'before' : {
                'tempF' : 5,
                'windSpeedMph' : 14,
                'windGustMph' : 14,
                'windDirection' : 'ESE',
                'precipInHr' : 0.1,
                'humidityPct' : 50,
                'conditions' : 'hail'
            },
            'midpoint' : {
                'tempF' : 6,
                'windSpeedMph' : 15,
                'windGustMph' : 16,
                'windDirection' : 'SE',
                'precipInHr' : 0.1,
                'humidityPct' : 50,
                'conditions' : 'sleet'
            }
        },
        'from' : {
            'before' : {
                'tempF' : 7,
                'windSpeedMph' : 16,
                'windGustMph' : 18,
                'windDirection' : 'S',
                'precipInHr' : 0.1,
                'humidityPct' : 50,
                'conditions' : 'wintrymix'
            },
            'midpoint' : {
                'tempF' : 8,
                'windSpeedMph' : 17,
                'windGustMph' : 19,
                'windDirection' : 'SW',
                'precipInHr' : 0.1,
                'humidityPct' : 50,
                'conditions' : 'snow'
            }
        }
    }
}

# endpoints

@app.route('/today/amrush', methods=['GET'])
def get_amRush():
    return jsonify({'samples': amWeatherData})

@app.route('/today/pmrush', methods=['GET'])
def get_pmRush():
    return jsonify({'samples': pmWeatherData})

# get commute am / pm weather for today & tomorrow
@app.route('/commuteWeatherTodayTomorrow', methods=['GET'])
def get_commuteWeatherTodayTomorrow():
    try:
        # get params
        windStation = request.args.get('windStation')
        tempStation = request.args.get('tempStation')
        toMidpoint = request.args.get('toMidpoint')
        fromMidpoint = request.args.get('fromMidpoint')

        # get current conditions
        tempStationConditions = get_urlJson(wundergroundBaseUrl + wundergroundApiKey + wundergroundConditions + wundergroundPwsPrefix + tempStation + wundergroundJsonSuffix)
        windStationConditions = get_urlJson(wundergroundBaseUrl + wundergroundApiKey + wundergroundConditions + wundergroundPwsPrefix + windStation + wundergroundJsonSuffix)

        # get forecast
        forecast = get_urlJson(wundergroundBaseUrl + wundergroundApiKey + wundergroundHourly + wundergroundPwsPrefix + tempStation + wundergroundJsonSuffix)

        # populate return
        # info
        returnJson['info']['asOf'] = tempStationConditions['current_observation']['observation_time_rfc822']
        returnJson['info']['tempStationLoc'] = tempStationConditions['current_observation']['observation_location']['full']
        returnJson['info']['windStationLoc'] = windStationConditions['current_observation']['observation_location']['full']

#TODO calc tomorrow, midpoint

        # today to now
        returnJson['today']['to']['now']['conditions'] = tempStationConditions['current_observation']['weather']
        returnJson['today']['to']['now']['humidityPct'] = tempStationConditions['current_observation']['relative_humidity'].replace('%', '')
        returnJson['today']['to']['now']['precipInHr'] = tempStationConditions['current_observation']['precip_1hr_in']
        returnJson['today']['to']['now']['tempF'] = tempStationConditions['current_observation']['temp_f']
        returnJson['today']['to']['now']['windDirection'] = windStationConditions['current_observation']['wind_dir']
        returnJson['today']['to']['now']['windGustMph'] = windStationConditions['current_observation']['wind_gust_mph']
        returnJson['today']['to']['now']['windSpeedMph'] = windStationConditions['current_observation']['wind_mph']

        # today to midpoint

        returnJson['today']['to']['midpoint']['conditions'] = '-'
        returnJson['today']['to']['midpoint']['humidityPct'] = -1
        returnJson['today']['to']['midpoint']['precipInHr'] = -1
        returnJson['today']['to']['midpoint']['tempF'] = -1
        returnJson['today']['to']['midpoint']['windDirection'] = '-'
        returnJson['today']['to']['midpoint']['windGustMph'] = -1
        returnJson['today']['to']['midpoint']['windSpeedMph'] = -1

        # today from before

        returnJson['today']['from']['before']['conditions'] = '-'
        returnJson['today']['from']['before']['humidityPct'] = -1
        returnJson['today']['from']['before']['precipInHr'] = -1
        returnJson['today']['from']['before']['tempF'] = -1
        returnJson['today']['from']['before']['windDirection'] = '-'
        returnJson['today']['from']['before']['windGustMph'] = -1
        returnJson['today']['from']['before']['windSpeedMph'] = -1

        # today from midpoint

        returnJson['today']['from']['midpoint']['conditions'] = '-'
        returnJson['today']['from']['midpoint']['humidityPct'] = -1
        returnJson['today']['from']['midpoint']['precipInHr'] = -1
        returnJson['today']['from']['midpoint']['tempF'] = -1
        returnJson['today']['from']['midpoint']['windDirection'] = '-'
        returnJson['today']['from']['midpoint']['windGustMph'] = -1
        returnJson['today']['from']['midpoint']['windSpeedMph'] = -1


#TODO: verify mday not just hr
#TODO: look at 'snow' *or* 'qpf'
        hourlyForecast = get_hourlyForecastIfExists(forecast, 17)

        if (hourlyForecast != None):
            returnJson['today']['from']['midpoint']['conditions'] = hourlyForecast['condition']
            returnJson['today']['from']['midpoint']['humidityPct'] = hourlyForecast['humidity']
            returnJson['today']['from']['midpoint']['precipInHr'] = hourlyForecast['qpf']['english']
            returnJson['today']['from']['midpoint']['tempF'] = hourlyForecast['temp']['english']
            returnJson['today']['from']['midpoint']['windDirection'] = hourlyForecast['wdir']['dir']
            returnJson['today']['from']['midpoint']['windGustMph'] = 0
            returnJson['today']['from']['midpoint']['windSpeedMph'] = hourlyForecast['wspd']['english']

        # tomorrow to before

        # tomorrow to midpoint

        # tomorrow from before

        # tomorrow from midpoint

        #        return jsonify({'weatherData': returnJson})
        return jsonify({'weatherData' : returnJson})
    except Exception as e:
        return make_response(jsonify({'weatherData' : { 'error': str(e)}}), 500)

def get_urlJson(url):
    response = requests.get(url)
    responseJson = response.json()
    if (response.status_code != httpSuccessCode):
        raise Exception('non-success code ' + str(response.status_code) + ' invoking: ' + url)

    if ('error' in responseJson['response']):
        raise Exception('error "' + responseJson['response']['error']['description'] + '" invoking: ' + url)

    return responseJson

def get_hourlyForecastIfExists(forecast, hr):
    for h in forecast['hourly_forecast']:
        fhr = int(h['FCTTIME']['hour'])
        if (fhr == hr):
            return h

    return None

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')