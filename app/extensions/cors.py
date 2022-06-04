from flask_cors import CORS
from  app.utils import Singleton


class Cors(Singleton):

    def __init__(self):
        
        self.app = None

    def init_app(self, app):
        r"""
        Documentation here
        """

        self.app = CORS(app)

        return app