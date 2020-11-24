from datetime import datetime


def date():
    date_today = datetime.today().strftime("%m/%d/%Y")
    return date_today
