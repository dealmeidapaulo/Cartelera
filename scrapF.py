#SCRAP farsamag.com

import lib.lib_soup_farsamag as farsamag
import lib.lib_soup as sp

import numpy as np
import pandas as pd


if __name__ == "__main__":
    F0  = pd.read_csv("data//df_x1.csv")
    F0  = F0["urlF"].to_list()
    F0 = [f for f in farsamag.Obras_getUrls() if f not in F0]
