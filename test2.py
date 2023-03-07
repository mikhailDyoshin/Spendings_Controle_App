import datetime
from handy import str2date

def months_order_list(startNumber:int) -> list:
    startNumber = startNumber
    return [i%12 for i in range(startNumber, startNumber+12)]

def months_list(monthsOrder:list) -> list:
    months = ('Jan.', 'Feb.', 'Mar.', 
          'Apr.', 'May', 'Jun.', 
          'Jul.', 'Aug.', 'Sep.', 
          'Oct.', 'Nov.', 'Dec.')
    
    return [months[index] for index in monthsOrder]


def months_list_former():
    today = datetime.date.today()

    currentMonth = today.month

    monthsOrder = months_order_list(currentMonth)

    selectedMonths = months_list(monthsOrder)   

    return selectedMonths


def month_shifter(date):
    yearAgoMonth = date.month
    if yearAgoMonth == 12:
        yearAgoShifted = date.replace(year = date.year + 1, month = 1, day = 1) 
    else:
        yearAgoShifted = date.replace(month = yearAgoMonth+1, day = 1)

    return yearAgoShifted


def date_identifier(date:str) -> dict:
    today = datetime.date.today()
    yearDelta = datetime.timedelta(days=365)
    yearAgoDate = today - yearDelta
    yearAgoShifted = month_shifter(yearAgoDate)

    return yearAgoShifted <= str2date(date) <= today


def dict_filter(dictionary:dict) -> dict:
    return {key: d[key] for key in list(filter(date_identifier, dictionary.keys()))}

d = {
    '2021.4.18': {'food': 250, 'transport': 10, 'shopping': 500, 'total': 760},
    '2022.4.18': {'food': 250, 'transport': 10, 'shopping': 500, 'total': 760},
    '2022.4.1': {'food': 250, 'transport': 10, 'shopping': 500, 'total': 760},
    '2023.2.18': {'food': 250, 'transport': 10, 'shopping': 500, 'total': 760},
    '2023.2.25': {'food': 25, 'transport': 100, 'shopping': 1000, 'total': 1125},
    '2023.3.3': {'food': 250, 'transport': 0, 'shopping': 1000, 'total': 1250},
    '2023.3.6': {'food': 250, 'transport': 100, 'shopping': 500, 'total': 1060},
}

print(months_list_former())

# print(dict_filter(d))
