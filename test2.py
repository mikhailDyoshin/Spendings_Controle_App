import datetime


def dates_list_former():
    # Today's date
    today = datetime.date.today()

    # Number of dates to create
    Ndays = 368

    # 368 days delta
    delta = datetime.timedelta(days=Ndays)

    # One day delta 
    dateIncrement = datetime.timedelta(days=1)

    # 368 days ago date
    yearAgo = today - delta

    # Empty list to store dates
    dates = []

    # The first element in the list
    date = yearAgo

    # Forms the dates list
    for i in range(Ndays):
        date += dateIncrement
        dates.append(str(date))

    return dates
    

dates_list = dates_list_former()

print(dates_list[0])