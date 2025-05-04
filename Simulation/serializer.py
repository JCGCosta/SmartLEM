import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

class PauloBorgesSerializer:
    def __init__(self):
        self.ds = []

    def get_data(self):
        return self.ds.copy()

    def upload_data(self, directory):
        pathlist = Path(directory).glob('**/*.csv')
        for path in pathlist:
            house_data = pd.read_csv(path, sep=",")
            if all(col in house_data.columns for col in
                   ["Residential_solar_generation", "Residential_wind_generation"]):
                house_data['Electricity_generation'] = house_data['Residential_solar_generation'] + house_data[
                    'Residential_wind_generation']
            elif "Residential_wind_generation" in house_data.columns:
                house_data['Electricity_generation'] = house_data['Residential_wind_generation']
            elif "Residential_solar_generation" in house_data.columns:
                house_data['Electricity_generation'] = house_data['Residential_solar_generation']
            else:
                house_data['Electricity_generation'] = np.zeros(len(house_data))
            house_data['Energy_Balance'] = house_data['Electricity_generation'] - house_data['Electricity_load']
            self.ds.append(house_data)

    def save_figures(self, save_dir: str):
        pd.set_option('display.max_columns', None)

        # for i, ds in enumerate(self.ds):
        #     ds['utc_timestamp'] = pd.to_datetime(ds['utc_timestamp'])
        #     ds.set_index('utc_timestamp', inplace=True)
        #     self.ds[i] = ds.resample('ME').sum()

        plt.figure(figsize=(24, 8))
        plt.title(f"Energy Consumption from Householders.")
        for i, ds in enumerate(self.ds):
            ds['Electricity_load'].plot(label=f"Householder-{i+1}")
        plt.legend()
        plt.savefig(f"{save_dir}/Energy_Consumption.png")

        plt.clf()
        plt.figure(figsize=(24, 8))
        plt.title(f"Electricity Generation from Householders.")
        for i, ds in enumerate(self.ds):
            ds['Electricity_generation'].plot(label=f"Householder-{i+1}")
        plt.legend()
        plt.savefig(f"{save_dir}/Energy_Generation.png")

        plt.clf()
        plt.figure(figsize=(24, 8))
        plt.title(f"Energy Balance from Householders.")
        for i, ds in enumerate(self.ds):
            ds['Energy_Balance'].plot(label=f"Householder-{i+1}")
        plt.legend()
        plt.savefig(f"{save_dir}/Energy_Balance.png")
        plt.clf()

if __name__ == '__main__':
    UseCase = PauloBorgesSerializer()
    UseCase.upload_data("UseCases/PauloBorges/Datasets")
    UseCase.save_figures("UseCases/PauloBorges/Results")