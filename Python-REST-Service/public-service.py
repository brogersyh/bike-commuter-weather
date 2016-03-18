#!flask/bin/python

from flask import Flask, jsonify

app = Flask(__name__)

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


@app.route('/today/amrush', methods=['GET'])
def get_amRush():
    return jsonify({'samples': amWeatherData})

@app.route('/today/pmrush', methods=['GET'])
def get_pmRush():
    return jsonify({'samples': pmWeatherData})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')