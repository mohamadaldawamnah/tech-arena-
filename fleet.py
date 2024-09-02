
import pandas as pd
from action import Action


class AllDatacenterData(object):

    def __init__(self):
        self.dd = pd.read_csv("data\datacenters.csv")

class AllServerData(object):

    def __init__(self):
        self.sd = pd.read_csv("data\servers.csv")

class SellingData(object):

    def __init__(self):
        self.selld = pd.read_csv("data\selling_prices.csv")

class ServerGen(object):

    def __init__(self, gen, all_server_data, dc_count, dc_id):
        self.generation = gen   # the server generation id
        self.x_s = {}   # id: x_s
        self.server_data = all_server_data.sd[all_server_data.sd["server_generation"]==self.generation]   # hold info about the specific server gen
        self.dc_count = dc_count
        self.id_counter = dc_id #used to give server ids


    def getserver_type(self):
        return self.server_data["server_type"].item()
    
    def getrelease_time(self):
        return self.server_data["release_time"].item()
    
    def getpurchase_price(self):
        return self.server_data["purchase_price"].item()
    
    def getslots_size(self):
        return self.server_data["slots_size"].item()
    
    def getenergy_consumption(self):
        return self.server_data["energy_consumption"].item()
    
    def getcapacity(self):
        return self.server_data["capacity"].item()
    
    def getlife_expectancy(self):
        return self.server_data["life_expectancy"].item()
    
    def getcost_of_moving(self):
        return self.server_data["cost_of_moving"].item()
    
    def getaverage_maintenance_fee(self):
        return self.server_data["average_maintenance_fee"].item()
    
    server_type = property(getserver_type)
    release_time = property(getrelease_time)
    purchase_price = property(getpurchase_price)
    slots_size = property(getslots_size)
    energy_consumption = property(getenergy_consumption)
    capacity = property(getcapacity)
    life_expectancy = property(getlife_expectancy)
    cost_of_moving = property(getcost_of_moving)
    average_maintenance_fee = property(getaverage_maintenance_fee)

    def __repr__(self):
        return f"{self.generation}| server count: {len(self.x_s)}"

    def get_purchase_ts(self, server_id):
        return self.x_s[server_id]
    
    def dismiss_server(self, server_id):
        self.x_s.pop(server_id)

    def add_server(self, server_id, purchase_ts):
        self.x_s[server_id] = purchase_ts

    def another_server_id(self):
        self.id_counter += self.dc_count
        # you can get back the dc_id by server_id%dc_count !!
        return self.id_counter

    def calc_capacity(self):
        # create a new data structure which keeps track of the servers available at t_s
        # actually this is a fucked up function because it would ideally require to have 168 fleets for all ts
        # then just have a function to get capacity at the current moment
        return self.capacity*len(self.x_s)


class DataCenter(object):

    def __init__(self, d_id, all_datacenter_data, selling_data):
        self.datacenter_id = d_id
        self.datacenter_data = all_datacenter_data.dd[all_datacenter_data.dd["datacenter_id"]==self.datacenter_id]
        self.servers = {}
        self.selling_prices = selling_data.selld[selling_data.selld["latency_sensitivity"]==self.latency_sensitivity]

    def __repr__(self):
        repr_str = f"{self.datacenter_id}\n"
        for s in self.servers.values():
            if len(s.x_s) >0:
                repr_str += f"\t{s.__repr__()}\n"
        return repr_str

    def getcost_of_energy(self):
        return self.datacenter_data["cost_of_energy"].item()
    
    def getlatency_sensitivity(self):
        return self.datacenter_data["latency_sensitivity"].item()
    
    def getslots_capacity(self):
        return self.datacenter_data["slots_capacity"].item()
    
    cost_of_energy = property(getcost_of_energy)
    latency_sensitivity = property(getlatency_sensitivity)
    slots_capacity = property(getslots_capacity)
    
    def get_server_selling_price(self, server_gen):
        return self.selling_prices[self.selling_prices["server_generation"]==server_gen]["selling_price"].item()

class Fleet(object):

    def __init__(self, ts):
        self.add = AllDatacenterData()
        self.selld = SellingData()
        self.asd = AllServerData()
        self.id_to_dc = {}
        self.datacenters = {}
        # initiate datacenters
        for i,dc_id in enumerate(self.add.dd["datacenter_id"]):
            self.datacenters[dc_id] = DataCenter(dc_id, self.add, self.selld)
            self.id_to_dc[i]=dc_id
        # init server_genereations in dcs
        dcs = self.datacenters.values()
        dc_count = len(dcs)
        for i, dc in enumerate(dcs):
            # print("i ", i, "|dc ", dc)
            for server_gen in self.asd.sd["server_generation"]:
                dc.servers[server_gen] = ServerGen(server_gen, self.asd, dc_count, i)
        self.timestep = ts

    def __repr__(self):
        repr_str = f"Fleet: at {self.timestep}\n"
        for dc in self.datacenters.values():
            repr_str += dc.__repr__()
        return repr_str
    
    def __str__(self):
        return self.__repr__()
    
    def get_average_maintenance_fee(self, action):
        # s_gen = action.server_generation
        return self.datacenters[action.datacenter_id].servers[action.server_generation].average_maintenance_fee
    
    # def get_dc_id(self, server_id): # does not work with moves
    #     return self.id_to_dc[server_id%len(self.datacenters)]
    
    # def get_purchase_time(self, action): # not used until the server is added
    #     dc = self.datacenters[action.datacenter_id]
    #     server = dc.servers[action.server_generation]
    #     return server.x_s[action.server_id]
    
    def get_life_expectancy(self, action):
        dc = self.datacenters[action.datacenter_id]
        server = dc.servers[action.server_generation]
        return server.life_expectancy
    
    def get_dc_cost_of_energy(self, action):
        dc = self.datacenters[action.datacenter_id]
        return dc.cost_of_energy
    
    def get_server_energy_consumption(self, action):
        dc = self.datacenters[action.datacenter_id]
        server = dc.servers[action.server_generation]
        return server.energy_consumption
    
    def get_server_purchase_price(self, action):
        dc = self.datacenters[action.datacenter_id]
        server = dc.servers[action.server_generation]
        return server.purchase_price
    
    def get_server_cost_of_moving(self, action):
        dc = self.datacenters[action.datacenter_id]
        server = dc.servers[action.server_generation]
        return server.cost_of_moving
    
    def get_server_selling_price(self, action):
        dc = self.datacenters[action.datacenter_id]
        return dc.get_server_selling_price(action.server_generation)
    
    def calc_server_capacity(self, action):
        dc = self.datacenters[action.datacenter_id]
        server = dc.servers[action.server_generation]
        return server.calc_capacity()
    
    def get_server_capacity(self, action):
        dc = self.datacenters[action.datacenter_id]
        server = dc.servers[action.server_generation]
        return server.capacity
    
    def get_dc_latency(self, action):
        dc = self.datacenters[action.datacenter_id]
        return dc.latency_sensitivity
    
    def add_server(self, dc, server_gen, server_id, purchase_time):
        dc = self.datacenters[dc]
        s_gen = dc.servers[server_gen]
        s_gen.add_server(server_id, purchase_time)

    def get_another_server_id(self, dc, server_gen):
        dc = self.datacenters[dc]
        s_gen = dc.servers[server_gen]
        s_id = s_gen.another_server_id()
        return s_id
    
    def get_available_server_for_purchase(self):
        available = []
        for s_id in self.asd.sd["server_generation"]:
            release_time = self.asd.sd[self.asd.sd["server_generation"]==s_id]["release_time"].item()
            release_time = release_time[1:-1].split(",")
            release_time = [int(item) for item in release_time]
            if self.timestep >= release_time[0] and self.timestep <= release_time[1]:
                available.append(s_id)
        # print(available)
        return available
    
class Fleets(object):

    def __init__(self, ts=168):
        self.timesteps = ts
        self.fleets = []
        for i in range(self.timesteps):
            self.fleets.append(Fleet(i+1))
    
    def get_fleet(self, ts):
        return self.fleets[ts-1]
    
    def __repr__(self):
        repr_str = ""
        for i in range(self.timesteps):
            ts = i+1
            repr_str += f"timestep: {ts}\n\t{self.get_fleet(ts).__repr__()}\n"
        return repr_str
    
    def __str__(self):
        return self.__repr__()
    
    def add_record(self, action, record):
        dc = action.datacenter_id
        s_gen = action.server_generation
        purchase_time = action.time_step
        s_id = self.get_fleet(purchase_time).get_another_server_id(dc, s_gen)
        action.server_id = s_id
        for row in record.record:
            ts = row[0]
            ts_fleet = self.get_fleet(ts)
            if row[2]:  #if the server moved in its run
                dc = row[2]
            ts_fleet.add_server(dc, s_gen, s_id, purchase_time)
        return action

if __name__ == "__main__":

    add = AllDatacenterData()
    selld = SellingData()
    asd = AllServerData()
    # server = ServerGen("CPU.S1", asd)
    # print(server.server_type)
    # dc = DataCenter("DC1", add, selld)
    # fleets = Fleets()
    # print(fleets)

    from action import Action

    ac = Action(1, "DC1", "CPU.S2", "1", "buy")
    # print(fleet.get_average_maintenance_fee(ac))

    fl = Fleet(1)
    fl.get_available_server_for_purchase()



