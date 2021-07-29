import tornado.web
import tornado.httpserver
import tornado.ioloop
import sys
import tornado.options
import logging
import socket

class ServerManager():
    def __init__(self, paths, port):
        self.paths = paths
        self.port = port
        self.threads = 1

    def start(self):
        self.application = tornado.web.Application(self.paths, cookie_secret="b77c3d333f167e7d1675182dcc8d22a7/Vo=", gzip=True, template_path='./templates', debug=True)
        self.http_server = tornado.httpserver.HTTPServer(self.application)
        self.http_server.listen(self.port)
        tornado.options.parse_command_line()
        tornado.ioloop.IOLoop.instance().start()
