import fleet 
from action import Action, Actions
from demand import Demand
import pandas as pd

class DecisionMaker(object):

    def __init__(self, d):
        self.actions = Actions()
        self.fleet = fleet.Fleet()
        self.demand = Demand(d)

    def create_solution(self):
        # implement the acutal algorithm here <------
        return self.actions.actions
    
