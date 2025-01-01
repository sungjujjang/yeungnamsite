def date_sliser(date):
    # dictionary
    # date = 'YYYYMMDDHHMMSS'
    date = {
        'year': date[0:4],
        'month': date[4:6],
        'day': date[6:8],
        'hour': date[8:10],
        'minute': date[10:12],
        'second': date[12:14]
    }
    return date

def make_date_text(slice_date):
    return f"{slice_date['month']}/{slice_date['day']} {slice_date['hour']}:{slice_date['minute']}"