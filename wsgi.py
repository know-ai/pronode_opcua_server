from app import CreateApp
from pyhades import PyHades, PyHadesContext
import logging


logging.basicConfig(filename='app.log',level=logging.DEBUG)

application = CreateApp()
app = application()
hades_app = PyHades()
mode = hades_app.get_mode()

logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger('peewee').setLevel(logging.WARNING)

if __name__ == "__main__":

    with PyHadesContext(hades_app):
        
        app.run(host="0.0.0.0", port=5000)