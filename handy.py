import datetime


def date2str(date):
    """
        Turns date-object to str-object.
    """
    return str(date)


def lastDatesSpendings(dates, spendings, period):
    today = datetime.date.today()
    
    datesDateType = map(lambda x: str2date(x), dates)

    data = dict(zip(datesDateType, spendings))
    
    lastDates = []
    for i in range(period-1, -1, -1):
        delta = datetime.timedelta(days=i)
        lastDates.append(today-delta)
    
    lastData = {}
    for key in lastDates:
        if key in data.keys():
            lastData[key] = data[key]
        else:
            lastData[key] = 0

    return (list(map(lambda x: str(x), lastData.keys())), list(lastData.values()))


def str2date(dateStr:str):
    """
        Translates string to date-object.
    """
    return datetime.date.fromisoformat(dateStr)
    

def sortByDate(rows, reverse=False):
    """ 
        Sorts list of tuples. 
        Each tuple has str-object with index '1' 
        that responses for a date when a record was made.
        Sorting is done by this element.
    """
    return sorted(rows, key=lambda record: str2date(record[1]), reverse=reverse)


def datesAndTotals(rows):
    """
        Returns two lists: one contains dates, the other one - total spendings.
    """
    dates = []
    spendings = []
    for row in rows:
            dates.append(row[1])
            spendings.append(row[5])

    return (dates, spendings)


def isoform2dmY(isoform:str) -> str:
    """ Translates date's format: YYYY-MM-DD --> DD.MM.YYYY """
    return str2date(isoform).strftime('%d.%m.%Y')


def dmY2isoform(dmY:str) -> str:
    """ Translates date's format: DD.MM.YYYY --> datetime.date-object """
    dateParts = dmY.split('.')

    day, month, year = list(map(lambda x: int(x), dateParts))

    return date2str(datetime.date(year, month, day))
