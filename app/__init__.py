import os
from flask import Flask
from pyhades import PyHades

app = Flask(__name__, instance_relative_config=False)

mode = os.environ.get('APP_MODE') or 'Development'
hades_app = PyHades()
hades_app.set_mode(mode)

class CreateApp():
    """Initialize the core application."""


    def __call__(self):
        """
        Documentation here
        """
        app.client = None
        
        with app.app_context():

            from . import modules
            _app = modules.init_app(app)

            from . import extensions
            extensions.init_app(_app)
            
            return _app
