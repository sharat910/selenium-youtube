import os
import time
import json
import sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_profile import AddonFormatError


class FirefoxProfileWithWebExtensionSupport(webdriver.FirefoxProfile):
    def _addon_details(self, addon_path):
        try:
            return super()._addon_details(addon_path)
        except AddonFormatError:
            try:
                with open(os.path.join(addon_path, 'manifest.json'), 'r') as f:
                    manifest = json.load(f)
                    print(manifest)
                    return {
                        'id': manifest['applications']['gecko']['id'],
                        'version': manifest['version'],
                        'name': manifest['name'],
                        'unpack': True,
                    }
            except (IOError, KeyError) as e:
                raise AddonFormatError(str(e), sys.exc_info()[2])

def get_adblock_profile(config):
    ffprofile = FirefoxProfileWithWebExtensionSupport()
    adblockfile = config['adblock']['file']
    ffprofile.add_extension(adblockfile)
    return ffprofile

def install_adblock(driver,config):
    adblockfile = config['adblock']['file']
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dir_path,adblockfile)
    driver.install_addon(filepath)
    time.sleep(1)
    handles = driver.window_handles
    driver.switch_to_window(handles[1])
    driver.close()
    driver.switch_to_window(handles[0])

def get_browser(config):
    desired_cap = None
    if config['browser'] == 'firefox':
        desired_cap = DesiredCapabilities.FIREFOX
    elif config['browser'] == 'chrome':
        desired_cap = DesiredCapabilities.CHROME
    return desired_cap

def get_local_driver(config):
    driver = None
    if config['browser'] == 'firefox':
        driver = webdriver.Firefox()
        if config['adblock']['enable']:
            #install_adblock(driver,config)
            driver = webdriver.Firefox(firefox_profile=get_adblock_profile(config))
    elif config['browser'] == 'chrome':
        driver = webdriver.Chrome()
    else:
        print("Browser type not supported!")

    return driver

def get_remote_driver(config):
    driver = None
    desired_cap = get_browser(config)
    if config['adblock']['enable']:
        ffprofile = get_adblock_profile(config)
        driver = webdriver.Remote(command_executor=config['hub_url'],
        desired_capabilities=desired_cap, browser_profile=ffprofile)
    else:
        driver = webdriver.Remote(command_executor=config['hub_url'],
        desired_capabilities=desired_cap)
    return driver

def get_driver(config):
    driver_type = config['type']
    if driver_type == 'remote':
        driver = get_remote_driver(config)
    elif driver_type == 'local':
        driver = get_local_driver(config)
    else:
        print("Incorrect driver type in configuration.")
    driver.set_window_position(0, 0)
    driver.set_window_size(config['width'],config['height'])
    return driver