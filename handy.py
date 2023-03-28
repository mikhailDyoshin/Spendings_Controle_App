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


def rgb_to_hex(rgb:tuple) -> str:
    return '#%02x%02x%02x' % rgb


def hex_to_rgb(hex:str) -> tuple:
    value = hex.lstrip('#')

    rgbList = [int(value[i:i+2], 16) for i in range(0, len(value), 2)]

    return tuple(rgbList)


def change_color(hexColor:str, incrTuple:tuple=(0, 0, 0)) -> str:
    rgbColor = hex_to_rgb(hexColor)
    
    rgbColorNew = tuple([(rgbColor[index]+incrTuple[index])%256 for index in range(len(rgbColor))])

    return rgb_to_hex(rgbColorNew)


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


def draw_power_symbol(exponent:int):
    """
        Forms a string like: 
        xbase^exponent but in unicode coding, 
        where "x" before "base" - is the multiplication cross, 
        ^exponent - an exponent in unicode coding.
    """
    powerCodes = {
        '0': '\u2070',
        '1': '\u00B9',
        '2': '\u00B2',
        '3': '\u00B3',
        '4': '\u2074',
        '5': '\u2075',
        '6': '\u2076',
        '7': '\u2077',
        '8': '\u2078',
        '9': '\u2079',
        '-': '\u207B',
    }

    base = 10

    powerStr = ''

    for char in str(exponent):
        powerStr += powerCodes[char] or ''

    return '\u00D7'+str(base)+powerStr


def get_exp_notation(number:float) -> tuple:

    """
        Returns a tuple that represents 
        the exponential notation 
        of a float number: 123.456 --> ('1.23', 2),
        where '1.23' is the base number 
        and 2 is its exponent.
    """

    expNotNum = '%.2E' % number

    baseNum , exponent = expNotNum.split('E')

    return (baseNum, int(exponent))


def float_to_exp_notation(number: float) -> str:
    """
        Takes a float number 
        and returns it exponential notation
        where its exponent is in unicode coding: 
        123.456 --> 1.23x10^2 or -0.0001 --> -1.00 
    """
    base, exponent = get_exp_notation(number)
    powerSymb = draw_power_symbol(exponent)

    return base + powerSymb
