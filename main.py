import random
import time
from youtube import YouTube
from config_parser import get_config
from flowfetch import FFInteractor
from driver import get_driver
import json

def get_video_list(config):
    with open(config['youtube']['video_list'],"r") as f:
        urls = [x.strip() for x in f.readlines()]
    return urls

def get_video_list_json(config):
    with open(config['video_list']) as f:
        videos = json.load(f)
    return videos

def get_playable_resolutions(config_res,available_res):
    return list(set(config_res) & set(available_res))

def play_with_res(url,res,config,f):
    print("Launching browser...")
    d = get_driver(config['driver'])
    y = YouTube(url,res, d, config['youtube'], f)
    y.play()
    time.sleep(2)

def play_one_video_all_resolutions(video):
    config = get_config()
    f = FFInteractor(config['flowfetch'])
    resolutions = get_playable_resolutions(config['resolutions'],video['resolutions'])
    print("Playing %s in" % (video['title']),resolutions)
    for res in resolutions:
        play_with_res(video['url'],res,config,f)

if __name__ == '__main__':
    ###########testing##########
    # config = get_config()
    # f = FFInteractor(config['flowfetch'])
    # play_with_res("https://www.google.com=1","360p",config,f)
    # import sys
    # sys.exit()
    ############################
    time.sleep(5)
    config = get_config()
    videos = get_video_list_json(config)
    n = min(len(videos),config['no_of_videos'])
    for video in videos[:n]:
        play_one_video_all_resolutions(video)