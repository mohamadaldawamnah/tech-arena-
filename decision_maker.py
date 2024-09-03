import fleet 
from action import Action, Actions
from demand import Demand
import pandas as pd
import math
from record import ActionRecord
from copy import deepcopy

class DecisionMaker(object):

    def __init__(self, d):
        self.actions = Actions()
        self.fleets = fleet.Fleets()
        self.timestep = 1
        # self.fleet = fleet.Fleet()
        self.demand = Demand(d)

    def get_current_fleet(self):
        return self.fleets.get_fleet(self.timestep)
    
    fleet = property(get_current_fleet)

    def create_solution(self):
        # implement the acutal algorithm here <------
        for ts in range(1, 169):
            self.handle_time_step(ts)
        return self.actions.actions
    
    def handle_time_step(self, ts):
        # just testing
        fleet = self.fleets.get_fleet(ts)
        available_servers = fleet.get_available_server_for_purchase()
        for dc in fleet.datacenters.keys():
            dc_servers = deepcopy(available_servers)
            i = 0
            while len(dc_servers)>0:
                s_gen = dc_servers[i]
                # for s_gen in dc_servers:
                action = Action(ts, dc, s_gen, None, "buy")
                if not self.handle_action(action):
                    dc_servers.pop(i)
                    if len(dc_servers) == 0:
                        break
                i = (i+1)%(len(dc_servers))


        # action = Action(ts, "DC1", "CPU.S1", None, "buy")
        # self.handle_action(action)
    
    def handle_action(self, action):
        record = self.E_buy(action)
        # print(record)
        e_limit = 500000
        if record.e > e_limit:
            updated_action = self.fleets.add_record(action, record)
            self.actions.add_action(updated_action)
            return True
        return False

    
    def E_buy(self, action):
        l = self.calc_max_l(action)
        record = ActionRecord(l, action.time_step)
        for ts in range(action.time_step, action.time_step + l):
            fleet = self.fleets.get_fleet(ts)
            e = self.calc_profit(action, fleet)# + self.p(fleet)*self.deltaUL(action, fleet)
            record.add_row(ts, e)
        record.maximize_by_dissmisal()
        print(f"Evaluation: {record.e}")
        return record
    
    def calc_max_l(self, action):
        x_s_hat = self.fleet.get_life_expectancy(action)
        max_l = 168 - action.time_step
        return min(x_s_hat, max_l)

#############################
# profit
    
    def calc_revenue(self, action, fleet):
        p = fleet.get_server_selling_price(action)
        satisfied_demand = self.calc_satisfied_demand(action,fleet)
        return satisfied_demand*p
    
    def calc_satisfied_demand(self, action, fleet):
        server_capacity = fleet.get_server_capacity(action)
        capacity = fleet.calc_server_capacity(action)
        dc_latency = fleet.get_dc_latency(action)
        demand = self.demand.get_ts_demand(fleet.timestep)[action.server_generation][dc_latency]
        # the demand needs reworking because it gives demand to a latency and not a specific datacenter
        # fix: get all capacities of dcs with that latency and then subtract from the demand the capacity of other dcs
        unsatisfied_demand = max(0,demand - capacity)
        satisfied_demand = min(unsatisfied_demand, server_capacity)
        # print(f"ts: {fleet.timestep}, demand: {demand}")
        return satisfied_demand


    def calc_cost(self, action, fleet):
        cost = self.calc_alpha(action, fleet) + self.calc_e_s(action, fleet)
        if action.action == "buy" and action.time_step == fleet.timestep:
            cost += fleet.get_server_purchase_price(action)
        # elif action.action == "move":
        #     cost += fleet.get_server_cost_of_moving(action)
        # print(f"cost: {cost}")
        return cost
    
    def calc_alpha(self, action ,fleet):
        b_s = fleet.get_average_maintenance_fee(action)
        x_s = fleet.timestep - action.time_step + 1 # amount of ts lived
        x_s_hat = fleet.get_life_expectancy(action) # life expextancy
        # print((3*x_s)/(2*x_s_hat))
        alpha = b_s * (1+((3*x_s)/(2*x_s_hat)) + math.log2((3*x_s)/(2*x_s_hat)))
        return alpha
    
    def calc_e_s(self, action, fleet):
        h_k = fleet.get_dc_cost_of_energy(action)
        e_s_hat = fleet.get_server_energy_consumption(action)
        return h_k*e_s_hat
    
    def calc_profit(self, action, fleet):
        revenue = self.calc_revenue(action, fleet)
        cost = self.calc_cost(action,fleet)
        profit = revenue - cost
        # print(f"profit: {profit}, timestep: {fleet.timestep}, revenue: {revenue}, cost: {cost}")
        return profit
    

#############################
# expected total profit

    def p(self, fleet):

        return 0
    
#############################
# difference in multipliers
    
    def deltaUL(self, action, ts):

        return 0


    
if __name__ == "__main__":

    import evaluation
    import action
    demand = pd.read_csv('./data/demand.csv')
    actual_demand = evaluation.get_actual_demand(demand)
    dm = DecisionMaker(actual_demand)
    # ac = action.Action(1, "DC1", "CPU.S1", "1", "buy")
    # dm.E_buy(ac)
    dm.handle_time_step(1)
    print(dm.fleets)
    print(dm.actions)