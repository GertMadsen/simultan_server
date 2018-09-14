import flask
import requests
import os
from datetime import datetime


my_app = flask.Flask(__name__)
user_file = './logs/clients.txt'
before = None

def write_page_to_file() :
    response = requests.get('https://news.ycombinator.com/')
    content_file = './templates/hackernews.html'
    with open(content_file,'w',encoding='utf-8') as file:
        file.write(response.text)             

def write_user_to_log(ip) :
    if (os.path.isfile(user_file)) :
        attr = 'a'
    else:
        attr = 'w'      
    
    with open(user_file,attr,encoding='utf-8') as file:
        file.write(f'{ip}\n')             


@my_app.before_request
def start_timer() :
    global before
    before = datetime.now()


@my_app.route('/')
def render_page() :
    write_user_to_log(flask.request.remote_addr) 
    return flask.render_template('hackernews.html')
    
@my_app.after_request
def end_timer() :
    global before
    after = datetime.now()
    serve_time = after - before
    with open(user_file,'a',encoding='utf-8') as file:
        file.write(f' - request served in {serve_time} miliseconds\n')


if __name__ == '__main__':
    write_page_to_file()
    my_app.run(host='0.0.0.0')


