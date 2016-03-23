#!/usr/bin/python
 # -*- coding: utf-8 -*-
 
import tornado.ioloop
import tornado.web
import logging
from Offensive import Offensive

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            text = self.get_argument("text", "")
            is_offensive = offensive.is_offensive(text)
            response = str(is_offensive)
            self.write(response)
        except Exception as e:
            logging.error(e.message)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    offensive = Offensive()
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()