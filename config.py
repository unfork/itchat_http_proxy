import json

class Config(object):
    # 默认配置
    _config = {
        'host': '127.0.0.1',
        'port': '7788',
        'debug': True,
        'static_path': 'static',
        'hot_reload': True
    }

    def __init__(self, config_file='config.json'):
        try:
            with open(config_file) as f:
                user_config = json.loads(f.read())
        except:
            user_config = {}
        self._config.update(user_config)

    def __getattr__(self, key):
        return self._config.get(key, None)

    def get(self, key):
        return self._config.get(key, None)
