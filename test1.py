from matplotlib import pyplot as plt
from test2 import *


def month_puller(date:str) -> list:
    """
        It takes a date like '2023.3.16'
        and returns the tuple that stores 
        the date(str) and the month of the date(int) 
        that is: 

        '2023.3.16' --> ('2023.3.16', 3).
    """
    return (date, int(date.split('.')[1]))

def zeros_list(length:int) -> list:
    """
        Creates a list of zeros with given length.
    """
    return [0 for x in range(length)]

def date_list_former(dictionary:dict) -> list:
    """
        Takes a dictionary 
        like {'2023.3.16': {}, '2023.3.17': {}, ...} 
        and using its keys 
        forms a list of tuples 
        like [('2023.3.16', 3), ('2023.3.17', 3), ...].
    """
    return list(map(lambda x: month_puller(x), dictionary.keys()))

def fieldsPuller(dictionary:dict):
    """
        Takes a dictionary like: 
        {
         'key1': {field1: ..., field2: ..., ..., fieldN: ...},
         'key2': {...}, ...,
         'keyM': {...}
        }
        and returns the list of fields, 
        that is [field1, field2, ..., fieldN].
    """
    return list(dictionary.values())[0].keys()

def empty_dict_for_plot_former(dictionary:dict) -> dict:
    """
        Takes a dictionary like: 
        {
         'key1': {field1: ..., field2: ..., ..., fieldN: ...},
         'key2': {...}, ...,
         'keyM': {...}
        }
        and creates a dictionary like:
        {
         'field1': [0, 0, ..., 0], 
         'field2': [...], 
          ..., 
         'fieldN': [...]
        },
        where each list stores 12 zeros.
    """
    return {key: zeros_list(12) for key in fieldsPuller(dictionary)}

def dict_for_plot_former(dictionary:dict, dictForPlot:dict, order:list) -> dict:
    """
        The function takes two dictionaries:

        {
         'key1': {field1: ..., field2: ..., ..., fieldN: ...},
         'key2': {...}, ...,
         'keyM': {...}
        } 

        and 

        {
         'field1': [0, 0, ..., 0], 
         'field2': [...], 
          ..., 
         'fieldN': [...]
        }

        and the list of numbers 
        that represents the order 
        of months to diplay on the plot.

        The second dictionary values are lists 
        formed in order that 'order'-argument defines.

        For example, if the sequence of months 
        that are going to be displayed on the plot is:

        ['Jun.', 'Jul.', ..., 'Apr.', 'May'], 
        
        then the lists in the second dictionary will look like:

        [TotalForJun, TotalForJul, ..., TotalForApr, TotalForMay]

        for each key.

    """
    for date, month in date_list_former(dictionary):
        index = order.index(month)
        for field in dictForPlot.keys():
            dictForPlot[field][index] += dictionary[date][field]

    return dictForPlot

def plot(dates:list, dictionary:dict):
    """
        The function builds the bar-plot.
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

emptyDictForPlot = empty_dict_for_plot_former(d)

dictForPlot = dict_for_plot_former(d, emptyDictForPlot, monthsOrderList)

plotFigure = plot(months, dictForPlot)

plt.show()
