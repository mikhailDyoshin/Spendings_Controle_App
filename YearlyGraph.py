from matplotlib.figure import Figure
from handy import str2date
import datetime


class YearlyGraph:
    def __init__(self, initDict):
        # The dictionary where all calculation start
        self.initDict = initDict

        # Months order
        self.monthOrder = self.months_order_list()

        # Months list (respresent how months will be displayed on the plot)
        self.monthsList = self.months_list_former()

        # Filtered dictionary that stores records made no later than one year ago
        self.filteredDict = self.dict_filter(self.initDict)

        # The dictionary for the plot which values are lists with zeros
        self.emptyDictFormPlot = self.empty_dict_for_plot_former(self.initDict)

        # The dictionary for the plot
        self.dictForPlot = self.dict_for_plot_former(
            self.filteredDict, 
            self.emptyDictFormPlot, 
            self.monthOrder)

        # The plot
        self.yearlyPlot = self.plot(self.monthsList, self.dictForPlot)


    """ *********** Methods that forms the list of months *********** """
    def months_order_list(self) -> list:
        """
            Takes the number of the current month 
            and forms a tuple of numbers 
            that tell in which order 
            to diplay all 12 months on the plot.

            For example, if the current month is March,
            that is its number is 3, 
            the tuple will be look like: 
            (3, 4, ..., 11, 0, 1, 2) 
            <=> ('Apr.', 'May', ..., 'Jan.', 'Feb.', 'Mar.') 
            if the default sequence of months is 
            ('Jan.', 'Feb.', ..., 'Dec.').
        """
        today = datetime.date.today()
        currentMonth = today.month
        return [i%12 for i in range(currentMonth, currentMonth+12)]


    def months_list(self, monthsOrder:list) -> list:
        """
            Forms the list of months in given order.
        """
        months = ('Jan.', 'Feb.', 'Mar.', 
            'Apr.', 'May', 'Jun.', 
            'Jul.', 'Aug.', 'Sep.', 
            'Oct.', 'Nov.', 'Dec.')
        
        return [months[index] for index in monthsOrder]


    def months_list_former(self):
        """
            Forms a list of months 
            which order is defined 
            by number of the current month. 

            For example, 
            if the current month is June,
            that is its number is 6, 
            the list of months will be look like:
            ['Jul.', 'Aug.', ..., 'May', 'Jun.']
        """
        monthsOrder = self.months_order_list()

        selectedMonths = self.months_list(monthsOrder)   

        return selectedMonths


    """ *********** Methods that filters the initial dictionary *********** """
    def month_shifter(self, today):
        """
            Shifts the date forward in time
            to the start of the following month:
            1) 2023.12.x -> 2024.1.1;
            2) 2023.x.y -> 2023.x+1.1, if x != 12.
        """
        yearDelta = datetime.timedelta(days=365)
        yearAgoDate = today - yearDelta

        yearAgoMonth = yearAgoDate.month
        if yearAgoMonth == 12:
            yearAgoShifted = yearAgoDate.replace(year=yearAgoDate.year+1, month=1, day=1) 
        else:
            yearAgoShifted = yearAgoDate.replace(month=yearAgoMonth+1, day=1)

        return yearAgoShifted


    def date_identifier(self, date:str) -> dict:
        """
            Identifies if the given date 
            is between the tommorow's date
            and the date x.y.1, 
            where
            - x=current_year-1, y=current_month+1,
            or 
            - x=current_year, y=1 if current_year=12.
        """
        today = datetime.date.today()
        yearAgoShifted = self.month_shifter(today)

        return yearAgoShifted <= str2date(date) <= today


    def dict_filter(self, dictionary:dict) -> dict:
        """
            Filters the given dictionary like:

            {'2021.4.18': {...},
            '2022.4.18': {...},
            '2022.4.1': {...},
            }

            and creates a new one
            that stores items which keys are dates
            that lie between the tommorow's date
            and the date x.y.1, 
            where
            - x=current_year-1, y=current_month+1,
            or 
            - x=current_year, y=1 if current_year=12.
        """
        return {key: dictionary[key] for key in list(filter(self.date_identifier, dictionary.keys()))}

    """ *********** Methods that creates a dictionary to build the plot *********** """
    def month_puller(self, date:str) -> list:
        """
            It takes a date like '2023.3.16'
            and returns the tuple that stores 
            the date(str) and the month of the date(int) 
            that is: 

            '2023.3.16' --> ('2023.3.16', 3).
        """
        return (date, datetime.date.fromisoformat(date).month)


    def zeros_list(self, length:int) -> list:
        """
            Creates a list of zeros with given length.
        """
        return [0 for x in range(length)]


    def date_list_former(self, dictionary:dict) -> list:
        """
            Takes a dictionary 
            like {'2023.3.16': {}, '2023.3.17': {}, ...} 
            and using its keys 
            forms a list of tuples 
            like [('2023.3.16', 3), ('2023.3.17', 3), ...].
        """
        return list(map(lambda x: self.month_puller(x), dictionary.keys()))


    def fieldsPuller(self, dictionary:dict):
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
        if dictionary:
            return list(dictionary.values())[0].keys()
        else:
            return []


    def empty_dict_for_plot_former(self, dictionary:dict) -> dict:
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
        return {key: self.zeros_list(12) for key in self.fieldsPuller(dictionary)}


    def dict_for_plot_former(self, dictionary:dict, dictForPlot:dict, order:list) -> dict:
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
        for date, month in self.date_list_former(dictionary):
            index = order.index(month-1)
            for field in dictForPlot.keys():
                dictForPlot[field][index] += dictionary[date][field]

        return dictForPlot


    def plot(self, months:list, dictionary:dict):
        """
            The function builds the bar-plot.
        """

        # the width of the bars: can also be len(x) sequence
        width = 0.6  

        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111)

        bottom = [0 for x in months]

        totalSpent = 0

        # Building the plot
        for field, fieldData in dictionary.items():
            if field != 'total': # to exclude the field "total"
                p = ax.bar(months, fieldData, width, label=field, bottom=bottom)

                for index, value in enumerate(fieldData):
                    bottom[index] += value

                ax.bar_label(p, label_type='center')
            else:
                totalSpent = sum(fieldData)

        ax.set_title(f'Spendings for the last year: {totalSpent} r.')
        ax.legend()

        return fig
