import matplotlib.pyplot as plt
import datetime


class Data():
    """ 
        The class is created to prepare the data 
        for displaying it in UI, 
        after the data was fetched from the database.
    """

    def __init__(self, data, fields):
        # The list of fetched data from the database
        self.data_sorted = self.sortByDate(data)

        # The list of fields in the database table
        self.fields = fields

        # The period
        self.period = 30

        # Initial dictionary formed with fetched data
        self.initDict = self.create_dict(self.data_sorted, self.fields)

        # The dictionary the stores all spendings done in the last period
        self.lastDatesSpendings = self.last_dates_spendings(self.initDict, self.fields, self.period)

        # The list of the last dates
        self.lastDatesSorted = list(self.lastDatesSpendings.keys())

        # The list of the last spendings
        self.lastDataSorted = list(self.lastDatesSpendings.values())

        # The dictionary needed to build the plot
        self.dictForPlot = self.dict_for_plot(self.lastDataSorted, self.fields)

        # The figure of the plot
        self.plotFig = self.plot(self.lastDatesSorted, self.dictForPlot)


    """ Methods """
    def sortByDate(self, rows:list, reverse:bool=False) -> list:
        """ 
            Sorts list of tuples. 
            Each tuple has str-object with index '1' 
            that responses for a date when a record was made.
            Sorting is done by this element.
        """
        return sorted(rows, key=lambda record: self.str2date(record[1]), reverse=reverse)


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
        listItemsSorted = sorted(listItems, key=lambda record: self.str2date(record[0]), reverse=reverse)

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


    def date2str(self, dates:list) -> list:
        """
            Turns date-object into str-object: (date object)2023-02-05 -> (str object)2023.2.5
        """
        return list(map(lambda x: self.date_thinner(str(x).replace('-', '.')), dates))


    def last_dates(self, period:int) -> list:
        """
            Forms the list of the last dates from today to today minus period.
        """
        today = datetime.date.today()

        return [today-datetime.timedelta(days=i) for i in range(period-1, -1, -1)]


    def last_dates_spendings(self, data_dict:dict, fields:list, period:int) -> dict:
        """
            Form the dictionary of day spendings records 
            that exist in database 
            and of those that haven't been recorded yet 
            (the last are defined as dictionaries with zeroes in fields).
        """
        lastDatesStr = self.date2str(self.last_dates(period))

        # The dictionary with 0s in its values
        zeroData = {fields[index]: 0 for index in range(len(fields))}

        # The dictionary of dictionaries: {date1: {field1: ..., field2: ...}, date2: {...}}
        zeroDict = {key: zeroData for key in lastDatesStr}

        # Forming the result dictionary of existing records and of those that haven't been recorded yet.
        for key in lastDatesStr:
            if key in data_dict.keys():
                zeroDict[key] = data_dict[key]
        
        return zeroDict


    def dict_for_plot(self, sortedListOfDicts:list, keys:list) -> dict:

        """
            Form the specific dictionary to draw a plot.
            The dictionary looks like this: 
            {field1: [..., ..., ...], field2: [..., ..., ...], ...}, 
            where each element of the list is field's record saved in particular day.
        """

        # Form a dictionary with values as empty lists
        dictForPlot = {key:[] for key in keys}
        
        # Form the result dictionary
        for dictionary in sortedListOfDicts:
            for key in dictionary:
                dictForPlot[key].append(dictionary[key])
        
        return dictForPlot


    def plot(self, dates:list, dictionary:dict):
        """
            The function builds the plot.
        """

        # the width of the bars: can also be len(x) sequence
        width = 0.6  

        fig, ax = plt.subplots()
        bottom = [0 for x in dates]

        # Building the plot
        counter = 0
        for field, fieldData in dictionary.items():
            counter += 1
            if counter < 4: # to exclude the last field (total)
                p = ax.bar(dates, fieldData, width, label=field, bottom=bottom)

                for index, value in enumerate(fieldData):
                    bottom[index] += value

                # ax.bar_label(p, label_type='center')

        # X-ticks
        xTicks = [el if index == 0 or index == len(dates)-1 else '' for index, el in enumerate(dates)]

        ax.set_title(f'Spendings for the last {self.period} days')
        ax.set_xticks(dates, xTicks)
        ax.legend()

        return fig
        # plt.show()


    def str2date(self, s:str):
        """
            Translates string to date-object
        """
        year, month, day = s.split('.')
        return datetime.date(int(year), int(month), int(day))
