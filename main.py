import os.path

import cherrypy

from sqlhandler import SQLHandler


class FHSCSC(object):

    @cherrypy.expose
    def index(self, email='default'):
        if email == 'default':
            return open('public/index.html')
        else:
            raise cherrypy.HTTPRedirect(
                "https://docs.google.com/forms/d/e/1FAIpQLScHv_lWhVAl2Ev3U2eCoHGvB1OrV5_puzISj523RPtg3vFPfw/viewform?usp=pp_url&entry.1045781291=" + email)


@cherrypy.expose
class FHSCSCRequests(object):

    @cherrypy.tools.accept(media='text/plain')
    def POST(self, text):
        handler.submit(text)

    def GET(self):
        return handler.threaded_select()


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

handler = SQLHandler()

webapp = FHSCSC()
webapp.submit = FHSCSCRequests()
app = cherrypy.tree.mount(webapp, '/', conf)

if __name__ == "__main__":
    cherrypy.quickstart(webapp, '/', conf)
