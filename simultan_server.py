import flask
import requests
import os
from datetime import datetime
from flask import request

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


@my_app.route('/')
def render_page():  
    # write_user_to_log(flask.request.remote_addr)   
        return flask.render_template('hackernews.html')

@my_app.after_request
def per_request_timer(response):
    #global before
    after = datetime.now()
    serve_time = after - flask.request.before

    timestamp = after.replace(microsecond=0)

    with open(user_file, 'a', encoding='utf-8') as file:
        file.write(
            f' {timestamp},{flask.request.remote_addr},{serve_time}\n')

    return response


if __name__ == '__main__':
    write_page_to_file()
    my_app.run(host='0.0.0.0')
