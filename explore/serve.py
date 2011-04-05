import tornado
import tornado.web
import tornado.websocket
import tornado.httpserver
import math

from clients import ClientHandler, MobileClient

# command line options
from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)
define("host", default="127.0.0.1", help="run on the given ip", type=str)


registered_clients = ClientHandler()

# main handler
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        new_client = MobileClient() 
        client_id = new_client.client_id
        registered_clients[new_client.client_id] = new_client
        
        print "Rendering, ", options.host, options.port, client_id
        
        self.render("content.html", 
                    websocket_server_host=options.host,
                    websocket_server_port=options.port,
                    client_id = client_id)

#
# websocket handler
#
class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print "WebSocket opened"

    def on_message(self, data):
        info = zip(["client_id", "ax", "ay", "az", "ai", "arAlpha", "arBeta", "arGamma"], data.split(":"))
        registered_clients[ info["client_id"] ].update(info)

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