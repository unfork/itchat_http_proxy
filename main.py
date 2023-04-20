from lib import itchat
from http_server import start_http_server
from itchat_helper import start_itchat
from config import Config
import threading

def main():
    # 初始化微信
    threading.Thread(target=start_itchat).start()

    # 启动http服务
    threading.Thread(target=start_http_server, args=(Config().server_host, Config().server_port)).start()

if __name__ == '__main__':
    main()