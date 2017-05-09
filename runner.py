import requests
import redis
import time 
import bs4
import json 
from constants import REDIS_KEY,JSON_URL


# this code is the scrapper worker which is responsible for 
# getting the content and storing it in redis

class Scrapper(object):

    def __init__(self, interval,url,scrapper,json=True):
        self.interval = interval
        self.url = url
        self.json = True
        self.redis = redis.Redis() # going with default port
        self.scrapper = scrapper

    def get_page(self,params=None):

        # this can be used in the future for more interpolated urls
        params = {} if params == None else params
        params["cat"] = "G"
        url = self.url.format(**params)
        print("getting content from {}".format(url))
        response = requests.get(url)
        return response.json() if self.json else response.content 


    def run(self):
        while True:
            print('sleeping for {} s.'.format(self.interval))
            time.sleep(self.interval)
            content = self.get_page() 
            listing = self.scrap(content)
            try:
                self.send_to_redis(listing)
            except Exception as e:
                print("error occured while sending data",e)

    def scrap(self,content):
        return self.scrapper(content)


    def send_to_redis(self,listing):
        print("sending data to redis at key {}".format(REDIS_KEY))
        self.redis.set(REDIS_KEY,json.dumps(listing))




def jsonScrapper(json):
    return json["data"]
    


if __name__ =="__main__":

    scrapper = Scrapper(5,JSON_URL,jsonScrapper)
    scrapper.run()

