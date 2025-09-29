from datetime import date, timedelta


def calc_days_until(date_to: date) -> int:
    '''
    Calculate the number of days until a given date.

    :param date_to: The target date to calculate days until.
    :return: The number of days until the target date.
    '''
    today = date.today()
    delta = date_to - today
    return delta.days if delta.days >= 0 else 0


def add_months_to_date(start_date: date, months: int) -> date:
    '''
    Add a specified number of months to a given date.

    :param start_date: The initial date to which months will be added.
    :param months: The number of months to add.
    :return: The new date after adding the specified number of months.
    '''
    month = start_date.month - 1 + months
    day = start_date.day
    year = start_date.year + month // 12
    try:
        new_date = date(year, month % 12 + 1, day)
    except ValueError as ex:
        new_date = start_date + timedelta(days=30)
    return new_date


def is_leap_year(year: int) -> bool:
    '''
    Check if a given year is a leap year.

    :param year: The year to check.
    :return: True if the year is a leap year, False otherwise.
    '''
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
