from urllib.request import urlopen
from requests import get
import json
import os

from flask import Flask,render_template,request

start_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
end_url = '?unitGroup=metric&include=days&key=48WYWPXP4MG3ZH3HM6G7QCG95&contentType=json'
app = Flask(__name__)
response = None

ENV_MODE = os.environ.get("ENV", "production")  # ברירת מחדל: production
BUILD_NUM = os.environ.get("BUILD_NUM", "N/A")


@app.route('/', methods=['GET', 'POST'])
def start():
    """start page
    first return the form page
    user send location
    function return result page
    """
    if request.method == 'GET':
        return render_template('form.html')
    location = request.form.get('location')
    try:
        data = get_data(location)
        return render_template('result.html', location = data[0][0], rows = data )
    except:
        return 'bad location, try again '
def get_data(location):
    """function get location
    det information from api return information lists in list
    """
    url = start_url + location + end_url
    #option 1
    json_data = urlopen(url.replace(' ', '%20'))
    data = json.loads(json_data.read())

    #option 2
    data = get(url).json()

    data = [[data['resolvedAddress'], data['days'][i]['datetime'], data['days'][i]['tempmax'], data['days'][i]['tempmin'],
             data['days'][i]['humidity']] for i in range(7)]
    return data
#def get_json(location):

@app.route('/result')
def print_data(url):

    return "hello world"



if __name__ == '__main__':
    app.run(host="0.0.0.0")
