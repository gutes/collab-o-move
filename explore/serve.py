import cherrypy

class MyApp:
    """ Sample request handler class. """

    def index(self):
        with open("content.html") as content:
            return content.read()

    index.exposed = True


    def exit(self):
        raise SystemExit(0)
    exit.exposed = True


cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8080,
                       })
cherrypy.quickstart( MyApp() )