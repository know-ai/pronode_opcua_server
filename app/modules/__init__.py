from .server import *


# Init Resources
def init_app(app):

    from .server.resources import init_app as init_server

    init_server()
    
    return app