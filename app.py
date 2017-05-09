import cherrypy
import redis 
import constants
import json
import os 

class StockShow(object):


    def __init__(self):
        self.redis = redis.Redis()  # using default port and host 

    @cherrypy.expose
    def index(self):  
        return open("index.html").read()


    # we are directly exposing all the stocks for now
    @cherrypy.tools.accept(media='application/json')
    @cherrypy.expose
    def api(self):
        return self.redis.get(constants.REDIS_KEY)



if __name__ =="__main__":

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    
    cherrypy.quickstart(StockShow(),"/",conf)