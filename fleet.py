
import pandas as pd

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

    def __init__(self, gen, all_server_data):
        self.generation = gen   # the server generation id
        self.x_s = {}   # id: x_s
        self.server_data = all_server_data.sd[all_server_data.sd["server_generation"]==self.generation]   # hold info about the specific server gen
        self.id_counter = 0 #used to give server ids


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
        return self.server_data["average_maintenance"].item()
    
    server_type = property(getserver_type)
    release_time = property(getrelease_time)
    purchase_price = property(getpurchase_price)
    slots_size = property(getslots_size)
    energy_consumption = property(getenergy_consumption)
    capacity = property(getcapacity)
    life_expectancy = property(getlife_expectancy)
    cost_of_moving = property(getcost_of_moving)
    average_maintenance_fee = property(getaverage_maintenance_fee)


class DataCenter(object):

    def __init__(self, d_id, all_datacenter_data, selling_data):
        self.datacenter_id = d_id
        self.datacenter_data = all_datacenter_data.dd[all_datacenter_data.dd["datacenter_id"]==self.datacenter_id]
        self.servers = {}
        self.selling_prices = selling_data.selld[selling_data.selld["latency_sensitivity"]==self.latency_sensitivity]

    def __repr__(self):
        return f"{self.datacenter_id}"

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

    def __init__(self):
        self.add = AllDatacenterData()
        self.selld = SellingData()
        self.asd = AllServerData()
        self.datacenters = {}
        for dc_id in self.add.dd["datacenter_id"]:
            self.datacenters[dc_id] = DataCenter(dc_id, self.add, self.selld)
        self.timeslot = 0

if __name__ == "__main__":

    add = AllDatacenterData()
    selld = SellingData()
    asd = AllServerData()
    # server = ServerGen("CPU.S1", asd)
    # print(server.server_type)
    # dc = DataCenter("DC1", add, selld)
    fleet = Fleet()
    print(fleet.datacenters)


