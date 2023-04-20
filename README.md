# itchat_http_proxy
by gpt

使用python itchat库提供微信服务，收到消息转发到配置的http地址，并使用flask提供一个http服务接收外部请求，并把内容转发给itchat发送出去，设计一个这样的项目架构，多文件的命名

架构设计：

1. main.py：主程序，负责监听微信消息，收到消息时将其转发到配置的http地址，并启动http接口服务

2. http_server.py：http服务，负责接收外部请求，并把内容转发给itchat发送出去

3. itchat_helper.py：微信助手，负责封装itchat库提供的接口，方便其他模块调用

4. config.py：配置文件，负责存储一些配置信息，比如http地址等

