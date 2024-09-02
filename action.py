# import json

class Action(object):

    def __init__(self, timestep, datacenter_id, server_gen, server_id, action):
        self.action_dict = { "time_step" : timestep ,
                        "datacenter_id" : datacenter_id ,
                        "server_generation" : server_gen ,
                        "server_id" : server_id ,
                        "action" : action }
        
    def gettime_step(self):
        return self.action_dict["time_step"]
    
    def getdatacenter_id(self):
        return self.action_dict["datacenter_id"]
    
    def getserver_generation(self):
        return self.action_dict["server_generation"]
    
    def getserver_id(self):
        return self.action_dict["server_id"]

    def setserver_id(self, s_id):
        self.action_dict["server_id"] = s_id
    
    def getaction(self):
        return self.action_dict["action"]
    
    time_step = property(gettime_step)
    datacenter_id = property(getdatacenter_id)
    server_generation = property(getserver_generation)
    server_id = property(getserver_id, setserver_id)
    action = property(getaction)

    def __repr__(self):
        repr_str = ""
        for key in self.action_dict.keys():
            repr_str += f"{key}: {self.action_dict[key]}"
        return repr_str
    


class Actions(object):

    def __init__(self):
        self._actions = []

    def add_action(self, action):
        self._actions.append(action.action_dict)

    def getactions(self):
        return self._actions
    
    actions = property(getactions)

    def __repr__(self):
        repr_str = ""
        for action in self._actions:
            repr_str += action.__repr__() + "\n"
        return repr_str



