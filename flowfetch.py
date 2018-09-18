import requests

class FFInteractor(object):
    """docstring for FlowFetchInteractor"""
    def __init__(self, config):
        self.config = config
        self.started = False
    
    def start(self,content_metadata):
        if self.config['enable']:
            url = self.config['start_url']
            requests.post(url,json=content_metadata)
            self.started = True

    def stop(self,success):
        print("Stopping Flowfetch with",success)
        if self.config['enable'] and self.started:
            url = self.config['stop_url']
            requests.post(url,json={'success':success})

    def post_video_stat(self,data):
        if self.config['enable'] and self.started:
            url = self.config['video_stat_url']
            requests.post(url,json=data)