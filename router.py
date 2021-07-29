#! python

# Required classes
import sys
import json
from bson import ObjectId
import urllib
import re

#Tornado Classes
import tornado.web
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor   # `pip install futures` for python2

#my Classes
from modules import shorten
from modules import webserver
from modules import helper 


class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        return

    def get(self):
        helper.checkCookie(self)
        response = {"success": "This is the web front end."}
        
        userSalt = helper.checkCookie(self)

        self.render("index.tpl", userSalt=userSalt)
        self.finish()


class urlHandler(tornado.web.RequestHandler):
    def initialize(self, shortMaster, storage):
        self.list = shortMaster
        self.storage = storage
    
    def options(self):
        # Adding headers for ajax calls and proper encoding
        helper.setheaders(self, 1)

    def post(self):
        response = {"success": "Yeah we could connect"}
        self.write(helper.renderJSON(response, self.get_argument('callback', None)))
        self.finish()

    def put(self):
        response = {"success": "We need to update the URL"}
        self.write(helper.renderJSON(response, self.get_argument('callback', None)))
        self.finish()
        return

    def get(self, key):
        key = self.get_arguments('key', False)
        print('key')
        response = {"success": "We need to redirect to the proper URL"}
        self.write(helper.renderJSON(response, self.get_argument('callback', None)))
        self.finish()

if __name__ == "__main__":
    try:
        # Initialize our class once
        shortMaster = shorten.ListMaster()
        storage = {"abcde": {'url': 'http://blah.com', 'clicks': 0, 'user': 'adlsfjdsf'}}

        # Router Paths
        paths = [
            (r"/", MainHandler, dict()),
            (r"/([a-zA-Z0-9]+)", urlHandler, dict(shortMaster=shortMaster, storage=storage))
        ]

        # Grab the port from args
        port = int(sys.argv[1])

        # Start the server
        print('Press CTRL+C to stop server and save urls in memory')
        webserver.ServerManager(paths, port).start()
        
    except KeyboardInterrupt:
        print(storage)
        print ("Time to kill the threads.")