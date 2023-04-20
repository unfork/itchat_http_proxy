from lib import itchat
from lib.itchat.content import *
from config import Config
import requests
import json
import time

@itchat.msg_register([TEXT])
def receive_msg(msg):
    data = icat_message(msg, False)
    if None == data:
        return
    #print("%s" % json.dumps(msg))

    r = requests.post(Config().callback_url, json=data)
    return None

@itchat.msg_register([VOICE,PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    data = icat_message(msg, False)
    if None == data:
        return

    #print("%s" % msg)
    msg.download("static/" + msg.fileName)
    typeSymbol = {PICTURE: 'img', VIDEO: 'vid'}.get(msg.type, 'fil')

    return '@%s@%s' % (typeSymbol, msg.fileName)

@itchat.msg_register([TEXT], isGroupChat=True)
def handler_group_msg(msg):
    data = icat_message(msg, True)
    if None == data:
        return
    #print("%s" % json.dumps(msg))

    requests.post(Config().callback_url, json=data)
    return None
   
def _check(func):
    def wrapper(msg, is_group):
        create_time = msg.CreateTime
          # 跳过1分钟前的历史消息
        time_interval = int(time.time()) - int(create_time)
        if Config().get("hot_reload") == True and time_interval > 5:
            if is_group:
                print("[WX]history skipped msgid {}\t{}\tgroup:{}\t{}\t{}".format(msg.MsgId, time_interval,msg.user.NickName,msg.Type,msg.Text))
            else:
                print("[WX]history skipped msgid {}\t{}\tfriend:{}\t{}\t{}".format(msg.MsgId, time_interval,msg.user.NickName,msg.Type,msg.Text))
            return
        return func(msg, is_group)

    return wrapper

@_check
def icat_message(msg, is_group=False):
    data = {}
    data['event'] = ('EventGroupMsg', 'EventFriendMsg')[is_group]

    data['robot_wxid'] = msg.ToUserName
    data['robot_name'] = ''
    data['type'] = msg.MsgType
    data['from_wxid'] = msg.FromUserName
    data['from_name'] = msg.user.NickName
    if is_group == True:
        data['final_from_wxid'] = msg.ActualUserName
        data['final_from_name'] = msg.ActualNickName
    else:
        data['final_from_wxid'] = msg.user.UserName 
        data['final_from_name'] = msg.user.NickName
    data['to_wxid'] = msg.ToUserName
    data['msgid'] =  msg.MsgId
    data['CreateTime'] = msg.CreateTime
    data['content'] =  msg.Content
    data['group_wxid'] = msg.FromUserName 
    data['msg_type'] = msg.type
    data['msg'] = msg.text

    if is_group == True:
        data['group_wxid'] = msg.FromUserName
        data['IsAt'] = msg.IsAt
        data['ChatRoomOwner'] = msg.user.ChatRoomOwner

    return data

def start_itchat(hot_reload=False):
    itchat.auto_login(enableCmdQR=2, hotReload=True)
    itchat.run()

def send_message(content, toUserName):
    itchat.send(content, toUserName=toUserName)