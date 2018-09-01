import os.path

import cherrypy

from sqlhandler import SQLHandler


class FHSCSC(object):

    @cherrypy.expose
    def index(self):
        return open('public/index.html')

@cherrypy.expose
class FHSCSCRequests(object):

    @cherrypy.tools.accept(media='text/plain')
    def POST(self, text):
        handler.submit(text)

    def GET(self):
        return handler.threaded_select()


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/submit': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    db = 'messages.db'
    handler = SQLHandler(db)

    webapp = FHSCSC()
    webapp.submit = FHSCSCRequests()
    cherrypy.quickstart(webapp, '/', conf)
