

class ActionRecord(object):

    def __init__(self, l, current_ts):
        # record the decision made in the E_b function in order to then write it into fleets and furthermore record the action in actions
        # so after evaluating a run of an action, we record the best possible estimated path for it, then decide if it is worth taking, if it is,
        # write it into actions and then update fleets based on that run

        self.record = [None]*l
        # for i, ts in enumerate(range(current_ts, l+1)):
        #     self.record[i] = [ts, None, None]
        self.timestep = current_ts
        self.e = None
        
    def add_row(self, ts, e, move=None):
        self.record[ts - self.timestep] = [ts, e, move]

    def maximize_by_dissmisal(self):
        # do not calculate this, just go ahead with the predictions and see when it becomes neg profits afterwards
        e_sum = 0
        e_sum_max = float("-inf")
        e_sum_max_ts = None
        for row in self.record:
            e_sum += row[1]
            if e_sum > e_sum_max:
                e_sum_max = e_sum
                e_sum_max_ts = row[0]
            # print(f"sum: {e_sum}, max_sum: {e_sum_max}, max_sum_ts: {e_sum_max_ts}")
        self.record = self.record[:e_sum_max_ts-self.timestep+1]
        # self.record[-1] = self.record[-1][:2] + ["dismiss"]
        self.e = e_sum_max

    

    

