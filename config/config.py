import json


def load_config():
    config = {}
    with open('config/config.json', 'r') as c:
        config = json.load(c)
    return config


config = load_config()
