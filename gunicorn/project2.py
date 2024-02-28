import os
from urllib.request import urlopen
from requests import get
import json
from flask import Flask, render_template, request, send_file
import datetime

app = Flask(__name__)
start_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
end_url = '?unitGroup=metric&include=days&key=48WYWPXP4MG3ZH3HM6G7QCG95&contentType=json'
history_file = 'history/history.json'
history_data = []
bg_color = os.environ.get('BG_COLOR', 'blue')


@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'GET':
        return render_template('form.html', background = bg_color)

    location = request.form.get('location')

    try:
        data = get_data(location)
        history_data.append({'location': location, 'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        print(history_file)
        with open(history_file, 'w') as file:
            json.dump(history_data, file)
        return render_template('result.html', location=data[0][0], rows=data)
    except:
        return 'bad location, try again '


@app.route('/history', methods=['GET'])
def show_history():
    return render_template('history.html', history=history_data)


@app.route('/download_history', methods=['GET'])
def download_history():
    return send_file(history_file, as_attachment=True)


def get_data(location):
    url = start_url + location + end_url
    # option 1
    json_data = urlopen(url.replace(' ', '%20'))
    data = json.loads(json_data.read())

    # option 2
    # data = get(url).json()

    data = [[data['resolvedAddress'], data['days'][i]['datetime'], data['days'][i]['tempmax'],
             data['days'][i]['tempmin'], data['days'][i]['humidity']] for i in range(7)]
    return data



if __name__ == "__main__":
    app.run(debug=True)

