import os
from datetime import datetime
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def get_config():
    with open("config.yaml") as f:
        config = load(f,Loader=Loader)
    auto_tag(config)
    return config

def auto_tag(config):
    if config['youtube']['tag'] == '<test-tag>':
        config['youtube']['tag'] = "%s-%s" % (os.getlogin(), str(datetime.now()))