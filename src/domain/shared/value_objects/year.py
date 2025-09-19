class Year(int):
    def __new__(cls, value: int):
        if value is None or value < 2000:
            raise ValueError('Year must be a positive integer greater than 2000')
        return int.__new__(cls, value)

    def __str__(self):
        return str(self)
