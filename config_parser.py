import os
import sys
from datetime import datetime
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def get_config():
    with open("config.yaml") as f:
        config = load(f,Loader=Loader)
    tag(config)
    return config

def tag(config):
    if config['youtube']['tag'] == '<test-tag>':
        print("Tag not set!!!")
        sys.exit()
        #config['youtube']['tag'] = "%s-%s" % (os.getlogin(), str(datetime.now()))