import tornado
import tornado.web
import tornado.websocket
import tornado.httpserver

# command line options
from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)
define("host", default="127.0.0.1", help="run on the given ip", type=str)


# main handler
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        
        self.render("content.html", 
                    websocket_server_host=options.host,
                    websocket_server_port=options.port)

#
# websocket handler
#
class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print "WebSocket opened"

    def on_message(self, message):
        print "acceleration-data:", message
        #self.write_message(u"You said: " + message)


    def on_close(self):
        print "WebSocket closed"

    
def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket",EchoWebSocket)
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
                
if __name__ == "__main__":
    main()