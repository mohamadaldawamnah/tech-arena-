

class Demand(object):

    def __init__(self, d):
        self.demand = d

    def get_ts_demand(self, ts):
        return self.demand.loc[self.demand["time_step"]==ts, ["server_generation","high","low","medium"]]
    


if __name__ == "__main__":
    pass


