from data import Data
import matplotlib.pyplot as plt


def print_dict(d:dict):
    print('\nd:{')
    for key in d:
        print(f'{key}: {d[key]}', end=',\n')
    print('}')

def print_list(l:list):
    print('\nl:[')
    for index, value in enumerate(l):
        print(f'l[{index}] = {value}', end=',\n')
    print(']')


data = [(1, '2023.2.25', 25, 100, 1000, 1125), 
        (3, '2023.3.3', 250, 0, 1000, 1250), 
        (2, '2023.2.18', 250, 10, 500, 760),
        (4, '2023.3.6', 250, 100, 500, 1060),
        ]

fields = ['food', 'transport', 'shopping', 'total']

dataEntity = Data(data, fields)

# print_list(dataEntity.data_sorted)

# print_dict(dataEntity.initDict)

# print_dict(dataEntity.lastDatesSpendings)

# print_dict(dataEntity.dictForPlot)

figureMonth = dataEntity.lastMonthPlotFig

figureWeek = dataEntity.lastWeekPlotFig

plt.show()
