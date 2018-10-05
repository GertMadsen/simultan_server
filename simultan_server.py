import flask
import requests
import os
from datetime import datetime
from time import sleep
from datetime import timedelta
from random import randint

#  from flask import request

my_app = flask.Flask(__name__)
user_file = './logs/clients.txt'
#before = None



def create_directory(directory_name):
    try:
        cwd = os.getcwd()
        path_for_file = os.path.join(cwd, directory_name)

        if not os.path.exists(path_for_file):
            os.makedirs(path_for_file)
    except OSError:
        pass


def write_page_to_file():
    response = requests.get('https://news.ycombinator.com/')

    create_directory("templates")

    content_file = './templates/hackernews.html'
    with open(content_file, 'w', encoding='utf-8') as file:
        file.write(response.text)


@my_app.before_request
def start_timer():
    #global before
    #before = datetime.now()
    # Sætter datetime på request objektet som before property
    flask.request.before = datetime.now()


@my_app.route('/<fname>')
def render_page(fname):
    flask.request.logging = False 
    return ""

@my_app.route('/')
def render_page2():
    flask.request.logging = True
    sleep(1)
    return flask.render_template('hackernews.html')

@my_app.after_request
def per_request_timer(response):
    after = datetime.now()
    serve_time = after - flask.request.before    
    timestamp = datetime.now().replace(microsecond=0)

    if flask.request.logging:
            with open(user_file, 'a', encoding='utf-8') as file:
                file.write(
                f' {timestamp}, {flask.request.remote_addr}, {serve_time.microseconds}\n')

    return response


if __name__ == '__main__':
    write_page_to_file()
    my_app.run(host='0.0.0.0')
