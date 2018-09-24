from driver import get_driver
import functools
import time

RETRY_LIMIT = 3
RETRY_DELAY = 0.01

def retry_if_failed(function):
    """
    A decorator that wraps the passed in function and re-executes it
    until the RETRY_LIMIT with a RETRY_DELAY between executions.
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        for i in range(RETRY_LIMIT):
            try:
                if i != 0:
                    print("Trying again...")
                resolutions = function(*args, **kwargs)
                if 'Auto' not in resolutions:
                    continue
                return resolutions
            except Exception as e:
                # log the exception
                err = "There was an exception in  "
                err += function.__name__
                print(err)
                print(e)
                time.sleep(RETRY_DELAY)
        print("Failed executing %s. Skipping video..." %function.__name__)
        return []
    return wrapper

def ad_present(driver):
    try:
        driver.find_element_by_class_name("videoAdUi")
        return True
    except:
        return False

@retry_if_failed
def fetch_resolutions(driver, url):
    driver.get(url)
    time.sleep(2)
    while(ad_present(driver)):
        time.sleep(1)
    sb = driver.find_element_by_css_selector('.ytp-button.ytp-settings-button')
    sb.click()
    try:
        elem = driver.find_element_by_css_selector('div.ytp-menuitem:nth-child(5) > div:nth-child(1)')
        elem.click()
    except:
        try:
            elem = driver.find_element_by_css_selector('div.ytp-menuitem:nth-child(4) > div:nth-child(1)')
            elem.click()
        except:
            elem = driver.find_element_by_css_selector('div.ytp-menuitem:nth-child(3) > div:nth-child(1)')
            elem.click()
    time.sleep(0.5)
    res = driver.find_elements_by_class_name("ytp-menuitem-label")
    return [item.text for item in res]


def get_playable_resolutions(config,url):
    print("Fetching available resolutions...")
    d = get_driver(config['driver'])
    available_res = fetch_resolutions(d,url)
    d.close()
    print("Video can be played in",available_res)
    return list(set(config['resolutions']) & set(available_res))
