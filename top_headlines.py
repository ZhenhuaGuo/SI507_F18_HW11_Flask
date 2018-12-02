from flask import Flask, render_template
from secrets_example import api_key
from datetime import datetime
import requests

app = Flask(__name__)

@app.route('/')
def home_page():
    return '''<h1>Welcome!</h1>'''

@app.route('/user/<user_name>')
def user_name(user_name):
    greeting = get_greeting()
    section = "technology"
    title_list = get_articles()
    return render_template('user.html', name=user_name, greeting=greeting, my_list=title_list, section=section)

def get_articles():
    baseurl = 'https://api.nytimes.com/svc/topstories/v2/technology.json'
    params={'api-key': api_key}
    data = requests.get(baseurl, params).json()
    results = data['results']
    title_list = []
    for r in results[0:5]:
        title_list.append(r['title']+' ('+r['url']+')')
    return title_list

# extra credit 1
@app.route('/user/<user_name>/<section>')
def user_name_1(user_name, section):
    greeting = get_greeting()
    title_list = get_articles_1(section)
    return render_template('user.html', name=user_name, greeting=greeting, my_list=title_list, section=section)

def get_articles_1(section):
    baseurl = 'https://api.nytimes.com/svc/topstories/v2/'
    params={'api-key': api_key}
    extendedurl = baseurl + section +'.json'
    data = requests.get(extendedurl, params).json()
    results = data['results']
    title_list = []
    for r in results[0:5]:
        title_list.append(r['title']+' ('+r['url']+')')
    return title_list
    
# extra credit 2
def get_greeting():
    now = datetime.now()
    time_string = str(now)
    hour_str = time_string[11:13]
    minite_str = time_string[14:16]
    hour_int = int(hour_str)
    minite_int= int(minite_str)
    if hour_int <= 12:
        if minite_int == 0:
            greeting = "Good moring"
        else:
            greeting = "Good afternoon"
    elif hour_int <= 16:
        if minite_int == 0:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

    elif hour_int <= 20:
        if minite_int == 0:
            greeting = "Good evening"
        else:
            greeting = "Good night"
    else:
        greeting = "Good night"
    return greeting
if __name__ == '__main__': 
    app.run(debug=True)