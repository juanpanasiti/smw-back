from datetime import date, timedelta

from src.domain.shared.helpers.dates import add_months_to_date, calc_days_until, is_leap_year


def test_calc_days_until_future_date():
    future_date = date.today() + timedelta(days=10)
    days = calc_days_until(future_date)
    assert days == 10, f'Expected 10, got {days}'


def test_calc_days_until_past_date():
    past_date = date.today() - timedelta(days=5)
    assert calc_days_until(
        past_date) == 0, f'Expected 0, got {calc_days_until(past_date)}'
    assert calc_days_until(
        past_date) == 0, f'Expected 0, got {calc_days_until(past_date)}'


def test_add_months_to_date():
    start_date = date(2023, 1, 31)
    new_date = add_months_to_date(start_date, 1)
    assert new_date == date(2023, 3, 2), f'Expected 2023-03-01, got {new_date}'

    new_date = add_months_to_date(start_date, 12)
    assert new_date == date(
        2024, 1, 31), f'Expected 2024-01-31, got {new_date}'

    start_date = date(2023, 1, 30)
    new_date = add_months_to_date(start_date, 1)
    assert new_date == date(2023, 3, 1), f'Expected 2023-03-01, got {new_date}'

    start_date = date(2023, 1, 29)
    new_date = add_months_to_date(start_date, 1)
    assert new_date == date(
        2023, 2, 28), f'Expected 2023-02-28, got {new_date}'

    start_date = date(2023, 3, 15)
    new_date = add_months_to_date(start_date, 6)
    assert new_date == date(
        2023, 9, 15), f'Expected 2023-09-15, got {new_date}'


def test_is_leap_year():
    assert is_leap_year(2020) is True, '2020 should be a leap year'
    assert is_leap_year(1900) is False, '1900 should not be a leap year'
    assert is_leap_year(2000) is True, '2000 should be a leap year'
    assert is_leap_year(2021) is False, '2021 should not be a leap year'
