from flask import Flask, request
from itchat_helper import send_message
from config import Config
import json

app = Flask(__name__, static_folder=Config().static_path)
@app.route('/')
def index():
    return 'Hello World!'

@app.route('/push', methods=['GET', 'POST'])
def push():
    data = request.get_json()
    send_message(data['msg'], toUserName=data['toUserName'])
    return '{"code":0}'

def start_http_server(host, port):
    app.run(host=host, port=port)
