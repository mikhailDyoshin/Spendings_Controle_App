from matplotlib import pyplot as plt
from test2 import *


def month_puller(date:str) -> list:
    return (date, int(date.split('.')[1]))

def zeros_list(length:int) -> list:
    return [0 for x in range(length)]

def date_list_former(dictionary:dict) -> dict:
    return list(map(lambda x: month_puller(x), dictionary.keys()))

def fieldsPuller(dictionary:dict):
    return list(dictionary.values())[0].keys()

def empty_dict_for_plot_former(dictionary:dict) -> dict:
    return {key: zeros_list(12) for key in fieldsPuller(dictionary)}

def dict_for_plot_former(dictionary:dict, dictForPlot:dict, order:list) -> dict:
    
    for date, month in date_list_former(dictionary):
        index = order.index(month)
        for field in dictForPlot.keys():
            dictForPlot[field][index] += dictionary[date][field]

    return dictForPlot

def plot(dates:list, dictionary:dict):
    """
        The function builds the plot.
    """

    # the width of the bars: can also be len(x) sequence
    width = 0.6  

    fig, ax = plt.subplots()
    bottom = [0 for x in dates]

    # Building the plot
    for field, fieldData in dictionary.items():
        if field != 'total': # to exclude the field "total"
            p = ax.bar(dates, fieldData, width, label=field, bottom=bottom)

            for index, value in enumerate(fieldData):
                bottom[index] += value

            ax.bar_label(p, label_type='center')

    ax.set_title(f'Spendings this year')
    ax.legend()

    return fig


# d = {
#     '2023.2.18': {'food': 250, 'transport': 10, 'shopping': 500, 'total': 760},
#     '2023.2.25': {'food': 25, 'transport': 100, 'shopping': 1000, 'total': 1125},
#     '2023.3.3': {'food': 250, 'transport': 0, 'shopping': 1000, 'total': 1250},
#     '2023.3.6': {'food': 250, 'transport': 100, 'shopping': 500, 'total': 1060},
# }

dSorted = {
    '2021.4.18': {'food': 250, 'transport': 10, 'shopping': 500, 'total': 760},
    '2022.4.1': {'food': 250, 'transport': 10, 'shopping': 500, 'total': 760},
    '2022.4.18': {'food': 250, 'transport': 10, 'shopping': 500, 'total': 760},
    '2023.2.18': {'food': 250, 'transport': 10, 'shopping': 500, 'total': 760},
    '2023.2.25': {'food': 25, 'transport': 100, 'shopping': 1000, 'total': 1125},
    '2023.3.3': {'food': 250, 'transport': 0, 'shopping': 1000, 'total': 1250},
    '2023.3.6': {'food': 250, 'transport': 100, 'shopping': 500, 'total': 1060},
}

d = dict_filter(dSorted)

monthsOrderList = months_order_list(3)

months = months_list_former()

dictForPlot = empty_dict_for_plot_former(d)

# print(dictForPlot)

# print(date_list_former(d))

print(dict_for_plot_former(d, dictForPlot, monthsOrderList))


plotFigure = plot(months, dictForPlot)

plt.show()