import os
import time
from datetime import datetime
import logging
import random
import requests
from pprint import pprint
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

DIVS = [1,2,3,4,5,9,10,11,12,15]
DIV_TO_KEY = {}
INTERVAL = 0.5
RETRY_LIMIT = 5

class YouTube(object):
    """docstring for YouTube"""
    def __init__(self, url, resolution, driver, config,flowfetch):
        self.url = url
        self.resolution = resolution
        self.config = config
        self.flowfetch = flowfetch
        self.driver = driver
        
    def get_video_id(self):
        return self.url.split("=")[1]

    def select_resolution(self):
        print("Selecting resolution...")
        for i in range(RETRY_LIMIT):
            try:
                if i != 0:
                    print("Trying again...")
                time.sleep(0.2)
                sb = self.driver.find_element_by_css_selector('.ytp-button.ytp-settings-button')
                sb.click()
                time.sleep(0.3)
                elem = self.driver.find_element_by_css_selector('div.ytp-menuitem:nth-child(5) > div:nth-child(1)')
                elem.click()
                break
            except Exception as e:
                print("Resolution selection got error",e)
                if i == RETRY_LIMIT-1:
                    print("Failed to select resolution. Skipping video...")
                    # self.stop()
                    # self.play()
                    return False
                time.sleep(0.2)

        time.sleep(1)
        try:
            res = self.driver.find_elements_by_class_name("ytp-menuitem-label")
            for item in res:
                #print(item.text)
                if item.text == self.resolution:
                    item.click()
                    print("Selected", self.resolution)
                    return True
        except:
            print("Encountered error",e)

        print("Unable to select resolution", self.resolution)
        return False

    def get_video_and_enable_stats(self):
        print("Loading url...")
        for i in range(RETRY_LIMIT):
            try:
                self.driver.get(self.url)
                time.sleep(0.3)
                movie_player = self.driver.find_element_by_id('movie_player')
                self.hover = ActionChains(self.driver).move_to_element(movie_player)
            except Exception as e:
                print("Encountered error while loading url...")
                print(e)
                if i == RETRY_LIMIT - 1:
                    print("Failed to load url. Skipping video...")
                    # self.stop()
                    # self.play()
                    return False
                else:
                    time.sleep(0.1)
                    continue
        return self.enable_stats(movie_player)

    def enable_stats(self,movie_player):
        enabled = False
        for i in range(RETRY_LIMIT):
            if not enabled:
                ActionChains(self.driver).context_click(movie_player).perform()
                options = self.driver.find_elements_by_class_name('ytp-menuitem')
                for option in options:
                    option_child = option.find_element_by_class_name('ytp-menuitem-label')
                    if option_child.text == 'Stats for nerds':
                        option_child.click()
                        enabled = True
                        print("Enabled stats collection.")
                        return enabled
                if not enabled:
                    print("Still not enabled!")
                    time.sleep(1)
                else:
                    break
        return enabled 

    def collect_stats(self):
        try:
            stat_dict = self.create_new_stat_dict()
            n = self.config['number_of_data_points']
            print("Started collecting... it'll take %d seconds." % (n/2))
            for i in range(n):
                start = time.time()
                stat_dict['Timestamp'] = str(datetime.now())
                if i % 4 == 0:
                    self.hover.perform()
                stat_dict['Current Seek'] = self.get_current_seek()
                for div_id in DIVS:
                    elem = self.driver.find_element_by_css_selector(".html5-video-info-panel-content > div:nth-child(%d) > span:nth-child(2)"%div_id)
                    stat_dict[DIV_TO_KEY[div_id]] = elem.text
                #pprint(stat_dict)
                self.flowfetch.post_video_stat(stat_dict)
                time_taken = time.time()-start
                #print("Time taken",time_taken)
                time.sleep(max(0,INTERVAL - time_taken))
            return True
        except Exception as e:
            print("Ecountered error",e)
            return False

    def get_current_seek(self):
        elem = self.driver.find_element_by_css_selector(".ytp-time-current")
        return elem.text

    def create_new_stat_dict(self):
        stat = {}
        stat['Timestamp'] = None
        stat['Current Seek'] = None
        print("\nCollecting following stats...")
        for div_id in DIVS:
            key = self.driver.find_element_by_css_selector(".html5-video-info-panel-content > div:nth-child(%d) > div:nth-child(1)"%div_id).text
            stat[key] = None
            print(div_id,key)
            #Populate DIV_TO_KEY dict
            DIV_TO_KEY[div_id] = key
        return stat

    def get_content_metadata(self):
        c = {
            'agent': self.config['agent'],
            'content_id': self.get_video_id(),
            'content_provider': self.config['content_provider'],
            'content_resolution': self.resolution,
            'session_id': self.driver.session_id
        }
        return c

    def play(self):
        print("Starting flowfetch...")
        self.flowfetch.start(self.get_content_metadata())
        time.sleep(2)
        if not self.get_video_and_enable_stats():
            self.stop(False)
            return

        if not self.select_resolution():
            self.stop(False)
            return
        
        if self.collect_stats():    
            self.stop(True)
        else:
            self.stop(False)

    def stop(self,success):
        print("Closing driver...")
        self.driver.close()
        print("Stopping flowfetch...")
        self.flowfetch.stop(success)
        print("Done\n\n")