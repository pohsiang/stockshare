import pandas as pd
import statistics

class PHAnalysis:

    def get_list_sd(self, data_list):
        data_list = list(map(float, data_list))
        return statistics.stdev(data_list)

    