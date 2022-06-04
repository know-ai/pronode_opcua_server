from flask_restx import Namespace, Resource, fields
from app.extensions.api import api
from app import hades_app
import pickle

opcua_server_machine = hades_app.get_machine('OPCUAServer')
ns = Namespace('OPCUA Server', description='OPCUA Server')

endpoint_model = api.model("endpoint_model", {
    'hostname': fields.String(required=True, description='OPCUA Server hostname'),
    'port': fields.Integer(required=True, description='OPCUA Server port')
})

address_space_model = api.model("address_space_model", {
    'folder_name': fields.String(required=True, description='OPCUA Server folder name for your variables')
})

load_data_model = api.model("load_data_model", {
    'path_folder': fields.String(required=True, description='Path folder where is the dataframe')
})


@ns.route('/endpoint')
class EndpointResource(Resource):

    @api.doc()
    @ns.expect(endpoint_model)
    def post(self):
        """
        Set Endpoint to your OPC UA Server
        """
        endpoint = ""
        try:
            hostname = api.payload['hostname']
            port = api.payload['port']
            endpoint = f'opc.tcp://{hostname}:{port}/OPCUA/ProNodeServer/'
            opcua_server_machine.server.set_endpoint(endpoint)

            result = {
                "data": {
                    "endpoint": endpoint
                }
            }

            return result, 200

        except Exception as _err:

            result = {
                "message": _err
            }

            return result, 500


@ns.route('/address_space')
class AddressSpaceResource(Resource):

    @api.doc()
    @ns.expect(address_space_model)
    def post(self):
        """
        Set Address Space folder to your OPC UA Server
        """
        folder_name = ""
        try:
            folder_name = api.payload['folder_name']
            
            # get Objects node, this is where we should put our nodes
            objects = opcua_server_machine.server.get_objects_node()
            # populating our address space
            address_space = objects.add_folder(opcua_server_machine.idx, folder_name)
            setattr(opcua_server_machine, "address_space", address_space)

            result = {
                "data": {
                    "adddress_space": folder_name
                }
            }

            return result, 200

        except Exception as _err:

            result = {
                "message": _err,
                "data": {
                    "address_space": folder_name
                }
            }

            return result, 500

@ns.route('/load_data')
class AddressSpaceResource(Resource):

    @api.doc()
    @ns.expect(load_data_model)
    def post(self):
        """
        Load Pandas DataFrame to create variables
        """
        path = api.payload['path_folder']

        with open(path, 'rb') as data_file:
            
            data = pickle.load(data_file)
            setattr(opcua_server_machine, 'data', data)

        for col in data.columns:
            opcua_server_machine.variables.update({
                f"{col}": opcua_server_machine.address_space.add_variable(opcua_server_machine.idx, f"{col}", 0.0)
            })
        
        count_limit = data.shape[0]
        counter = 0
        setattr(opcua_server_machine, 'count_limit', count_limit)
        setattr(opcua_server_machine, 'counter', counter)

@ns.route('/run_server')
class RunServerResource(Resource):

    @api.doc()
    def post(self):
        """
        Run OPCUA Server

        To run the opcua server you must have configured some issues.

        - OPCUA Server Endpoint.
        - OPCUA Server Address Space.
        - Load Data from DataFrame
        """
        opcua_server_machine.server.start()
        opcua_server_machine.transition(to="running")
        