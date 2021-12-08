import requests


class NetworkService:

    def get(self, url: str):
        '''Wrapper around the requests module'''
        r = requests.get(url)
        return r.json()
