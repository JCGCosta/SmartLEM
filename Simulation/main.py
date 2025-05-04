from simulation import Simulation
from serializer import PauloBorgesSerializer

if __name__ == '__main__':
    UseCase = PauloBorgesSerializer()
    UseCase.upload_data("UseCases/PauloBorges/Datasets")
    data = UseCase.get_data()
    s = Simulation(data, 0.24, 0.01, 0.16)
    data, pricing = s.run(aggregate="month")
    data.to_csv("UseCases/PauloBorges/Results/SimulationData.csv")
    pricing.to_csv("UseCases/PauloBorges/Results/PricingResults.csv")