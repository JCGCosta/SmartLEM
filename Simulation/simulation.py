from unittest import case

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calc_prosumer_energy(row):
    if row["Total"] > 0: return 1.0
    return row["Produced_Energy"] / abs(row["Consumed_Energy"])

def calc_grounded_energy(row):
    if row["Total"] < 0: return 0.0
    return row["Total"] / row["Produced_Energy"]

def convert_to_hour(df):
    df['utc_timestamp'] = pd.to_datetime(df['utc_timestamp'])
    df.set_index('utc_timestamp', inplace=True)
    return df.resample('h').sum()

def convert_to_day(df):
    df['utc_timestamp'] = pd.to_datetime(df['utc_timestamp'])
    df.set_index('utc_timestamp', inplace=True)
    return df.resample('D').sum()

def convert_to_month(df):
    df['utc_timestamp'] = pd.to_datetime(df['utc_timestamp'])
    df.set_index('utc_timestamp', inplace=True)
    return df.resample('ME').sum()

class Simulation:
    def __init__(self,
                 data: [pd.DataFrame],
                 company_small_selling_bid: float = 0.24,
                 company_buying_bid: float = 0.01,
                 prosumers_bid: float = 0.16):
        self.data = data
        self.c_small_bid = company_small_selling_bid
        self.c_buying_bid = company_buying_bid
        self.p_bid = prosumers_bid

    def pricing(self, row, i):
        if row[f"Energy_Balance_{i}"] > 0:
            return (row[f"Energy_Balance_{i}"] * self.p_bid) * (1-row["Grounded_Energy%"])
        return (row[f"Energy_Balance_{i}"] * (1-row["Prosumer_Energy%"])) * self.c_small_bid + \
        (row[f"Energy_Balance_{i}"] * row["Prosumer_Energy%"]) * self.p_bid

    def run(self, aggregate: str = ""):
        pd.set_option('display.max_columns', None)
        dt = pd.DataFrame()
        for i, ds in enumerate(self.data):
            dt[f"Energy_Balance_{i}"] = ds["Energy_Balance"]
        dt["Total"] = dt.sum(axis=1)
        dt.insert(0, "utc_timestamp", self.data[0]["utc_timestamp"])
        match aggregate:
            case "hour": dt = convert_to_hour(dt)
            case "day": dt = convert_to_day(dt)
            case "month": dt = convert_to_month(dt)
        energy_columns = [col for col in dt.columns if col.startswith('Energy_Balance_')]
        dt['Produced_Energy'] = dt[energy_columns].apply(lambda row: row[row > 0].sum(), axis=1)
        dt['Consumed_Energy'] = dt[energy_columns].apply(lambda row: row[row < 0].sum(), axis=1)
        dt['Prosumer_Energy%'] = dt.apply(calc_prosumer_energy, axis=1)
        dt['Grounded_Energy%'] = dt.apply(calc_grounded_energy, axis=1)
        pricing = pd.DataFrame()
        for i, b in enumerate(energy_columns):
            pricing[f"Bill_{i}"] = dt.apply(self.pricing, args=(i,), axis=1)
        pricing_columns = [col for col in pricing.columns if col.startswith('Bill')]
        pricing["Bill_Trading_Company"] = round(pricing[pricing_columns].sum(axis=1), 4)
        return dt, pricing



