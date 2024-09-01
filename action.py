# import json

class Action(object):

    def __init__(self, timestep, datacenter_id, server_gen, server_id, action):
        self.action_dict = { "time_step" : timestep ,
                        "datacenter_id" : datacenter_id ,
                        "server_generation" : server_gen ,
                        "server_id" : server_id ,
                        "action" : action }


class Actions(object):

    def __init__(self):
        self._actions = []

    def add_action(self, action):
        self._actions.append(action.action_dict)

    def getactions(self):
        return self._actions
    
    actions = property(getactions)



