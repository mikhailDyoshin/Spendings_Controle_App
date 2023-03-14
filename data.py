import datetime
from handy import date2str, str2date
from matplotlib.figure import Figure


class Data():
    """ 
        The class is created to prepare the data, 
        after the data was fetched from the database,
        for displaying it in UI.
    """

    def __init__(self, data, fields):
        # The list of fetched data from the database
        self.dataSorted = self.sortByDate(data)

        # The list of fetched data from the database 
        # sorted from the most recent date to the latest one
        self.dataSortedReverse = self.sortByDate(data, reverse=True)

        # The list of fields in the database table
        self.fields = fields

        # The month period (30 days)
        self.month = 30

        # The week period (7 days)
        self.week = 7

        # Initial! dictionary formed with fetched data
        self.initDict = self.create_dict(self.dataSorted, self.fields)

        # The dictionaries that stores all spendings done in the last period
        self.lastMonthDatesSpendings = self.last_dates_spendings(self.month)
        self.lastWeekDatesSpendings = self.last_dates_spendings(self.week)

        # The lists of the last dates
        self.lastMonthDatesSorted = list(self.lastMonthDatesSpendings.keys())
        self.lastWeekDatesSorted = list(self.lastWeekDatesSpendings.keys())

        # The lists of the last spendings
        self.lastMonthDataSorted = list(self.lastMonthDatesSpendings.values())
        self.lastWeekDataSorted = list(self.lastWeekDatesSpendings.values())

        # The dictionaries needed to build the plot
        self.lastMonthDictForPlot = self.dict_for_plot(self.lastMonthDataSorted)
        self.lastWeekhDictForPlot = self.dict_for_plot(self.lastWeekDataSorted)

        # The figures of the plots for the last periods spendings
        self.lastMonthPlotFig = self.plot(self.lastMonthDatesSorted, 
        self.lastMonthDictForPlot, 
        self.month)

        self.lastWeekPlotFig = self.plot(self.lastWeekDatesSorted, 
        self.lastWeekhDictForPlot, 
        self.week)


    """ Methods """
    def sortByDate(self, rows:list, reverse:bool=False) -> list:
        """ 
            Sorts list of tuples. 
            Each tuple has str-object (it's index in the tuple is 1(one)) 
            that responses for a date when a record was made.
            Sorting is done by this element 
            from the latest date to the most recent.
        """
        return sorted(rows, key=lambda record: str2date(record[1]), reverse=reverse)


    def create_dict(self, data:list, fields:list) -> dict:
        """
            Creates a dictionary that looks like this: 
            {date1: {field11: ..., field12: ...}, date2: {...}}
        """
        # Forms list of dates
        dates = [day[1] for day in data]
        # Form list of every day spendings
        spendings = [ {fields[index-2]: value for index, value in enumerate(day) if index > 1} for day in data ]
    
        return dict(zip(dates, spendings))


    def sort_dict_bydate(self, dictionary:dict, reverse=False) -> dict:
        """
            Sorts a dictionary by keys as dates.
        """
        listItems = list(dictionary.items())
        listItemsSorted = sorted(listItems, key=lambda record: str2date(record[0]), reverse=reverse)

        lastDatesSorted = [date[0] for date in listItemsSorted]

        lastDataSorted = [date[1] for date in listItemsSorted]

        return dict(zip(lastDatesSorted, lastDataSorted))


    def date_thinner(self, date):
        """
            Deletes unneccery zero in a date: 2023.02.05 -> 2023.2.5.
        """
        if date[5] and date[8] == '0':
            return date[0:5]+date[6:8]+date[9:]
        elif date[8] == '0':
            return date[0:8]+date[9:]
        elif date[5] == '0':
            return date[0:5] + date[6:]


    def date2strList(self, dates:list) -> list:
        """
            Turns date-object into str-object: (date object)2023-02-05 -> (str object)2023.2.5
        """
        return list(map(lambda x: date2str(x), dates))


    def last_dates(self, period:int) -> list:
        """
            Forms the list of the last dates from today to today minus period.
        """
        today = datetime.date.today()

        return [today-datetime.timedelta(days=i) for i in range(period-1, -1, -1)]


    def last_dates_spendings(self, period:int) -> dict:
        """
            Form the dictionary of day spendings records 
            that exist in database 
            and of those that haven't been recorded yet 
            (the last are defined as dictionaries with zeroes in fields).
        """
        data_dict = self.initDict

        fields = self.fields

        lastDatesStr = self.date2strList(self.last_dates(period))

        # The dictionary with 0s in its values
        zeroData = {fields[index]: 0 for index in range(len(fields))}

        # The dictionary of dictionaries: {date1: {field1: ..., field2: ...}, date2: {...}}
        zeroDict = {key: zeroData for key in lastDatesStr}

        # Forming the result dictionary of existing records and of those that haven't been recorded yet.
        for key in lastDatesStr:
            if key in data_dict.keys():
                zeroDict[key] = data_dict[key]
        
        return zeroDict


    def dict_for_plot(self, sortedListOfDicts:list) -> dict:

        """
            Form the specific dictionary to draw a plot.
            The dictionary looks like this: 
            {field1: [..., ..., ...], field2: [..., ..., ...], ...}, 
            where each element of the list is field's record saved in particular day.
        """

        keys = self.fields

        # Form a dictionary with values as empty lists
        dictForPlot = {key:[] for key in keys}
        
        # Form the result dictionary
        for dictionary in sortedListOfDicts:
            for key in dictionary:
                dictForPlot[key].append(dictionary[key])
        
        return dictForPlot


    def plot(self, dates:list, dictionary:dict, period:int):
        """
            The function builds the plot.
        """

        # the width of the bars: can also be len(x) sequence
        width = 0.6  

        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111)


        bottom = [0 for x in dates]

        # Building the plot
        for field, fieldData in dictionary.items():
            if field != 'total': # to exclude the last field (total)
                p = ax.bar(dates, fieldData, width, label=field, bottom=bottom)

                for index, value in enumerate(fieldData):
                    bottom[index] += value
            else:
                totalSpent = sum(fieldData)

        # X-ticks
        xTicks = [el if index == 0 or index == len(dates)-1 else '' for index, el in enumerate(dates)]

        ax.set_title(f'Spendings for the last {period} days: {totalSpent} r.')
        ax.set_xticks(dates, xTicks)
        ax.legend()

        return fig
