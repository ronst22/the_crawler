import tornado.ioloop
import tornado.web
import logging
from Offensive import Offensive

class MainHandler(tornado.web.RequestHandler):
    def __init__(self):
        self.offensive = Offensive()

    def post(self):
        try:
            text = self.get_argument("text", "")

            response = {"offensive" : self.offensive.is_offensive(text)}
            self.write(response)
        except Exception as e:
            logging.error(e.message)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()