from app.extensions.api import api


def init_app():

    from .server import ns as ns_server

    api.add_namespace(ns_server, path="/opcua/server")