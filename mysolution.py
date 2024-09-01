
import numpy as np
import pandas as pd
from seeds import known_seeds
from utils import save_solution
from evaluation import get_actual_demand
from decision_maker import DecisionMaker

from demand import Demand

def get_my_solution(d):
    dm = DecisionMaker(d)
    return dm.create_solution()


seeds = known_seeds('training')

demand = pd.read_csv('./data/demand.csv')

for seed in seeds[:1]:
    # SET THE RANDOM SEED
    np.random.seed(seed)

    # GET THE DEMAND
    actual_demand = get_actual_demand(demand)
    # actual_demand.to_csv("actual_demand.csv", index=False)    # if you want to see the actual_demand in csv file

    # CALL YOUR APPROACH HERE
    solution = get_my_solution(actual_demand)

    # SAVE YOUR SOLUTION
    save_solution(solution, f'./output/{seed}.json')

