import pandas as pd
from evaluation import get_actual_demand

class Demand(object):

    def __init__(self, d):
        self.demand = d

    def get_ts_demand(self, ts):
        ts_demand = self.demand.loc[self.demand["time_step"]==ts, ["server_generation","high","low","medium"]]
        ts_demand_dict = {}
        for s_gen in ts_demand["server_generation"]:
            row = ts_demand[ts_demand["server_generation"]==s_gen]
            ts_demand_latency = {"low": row["low"].item(),
                                 "medium": row["medium"].item(),
                                 "high": row["high"].item()}
            ts_demand_dict[s_gen] = ts_demand_latency
        return ts_demand_dict


if __name__ == "__main__":
    demand = pd.read_csv('./data/demand.csv')
    actual_demand = get_actual_demand(demand)
    d = Demand(actual_demand)
    print(d.get_ts_demand(2))


