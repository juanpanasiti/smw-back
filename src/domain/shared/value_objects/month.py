class Month(int):
    def __new__(cls, value: int):
        if value is None or not (1 <= value <= 12):
            raise ValueError('Month must be between 1 and 12')
        return int.__new__(cls, value)

    def __str__(self):
        return f'{self:02d}'
