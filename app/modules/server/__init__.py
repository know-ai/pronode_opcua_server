from pyhades import PyHades, PyHadesStateMachine, State
from opcua import Server as OPCUAServer

app = PyHades()

@app.define_machine(name='OPCUAServer', interval=1.0, mode="async")
class OPCUAServer(PyHadesStateMachine):

    # states
    standby = State('Standby', initial=True)
    running = State('Running')
    resetting  = State('Resetting')
    # transitions
    standby_to_running = standby.to(running)
    running_to_resetting = running.to(resetting)
    resetting_to_standby = resetting.to(standby)

    server = OPCUAServer()
    priority = 0

    def __init__(self, name):

        super().__init__(name)
        # setup our own namespace, not really necessary but should as spec
        uri = "http://examples.freeopcua.github.io"
        self.idx = self.server.register_namespace(uri)

        # Variables to Serve in OPCUA Sever
        self.variables = dict()

    def while_standby(self):
        r"""
        Documentation here
        """
        self.priority = 1


    def while_running(self):
        r"""
        Documentation here
        """
        # Update Values
        self.update()

        if self.counter >= self.count_limit - 1:

            self.counter = 0
        
        else:
            # Increment counter
            self.counter += 1

    def while_resetting(self):
        r"""
        Documentation here
        """
        self.resetting_to_starting()

    def update(self):
        r"""
        Set values into OPCUA Server
        """
        for key, value in self.variables.items():

            set_value = getattr(value, 'set_value')
            set_value(round(self.data[f'{key}'].values[self.counter], 4))

    def transition(self,to):
        r"""
        Documentation here
        """
        _from = self.current_state.name.lower()
        _transition = getattr(self, '{}_to_{}'.format(_from, to))
        _transition()
