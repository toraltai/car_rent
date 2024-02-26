from enum import Enum


class Period(str, Enum):
    first = '3 месяца',
    second = '6 месяцов',


class Role(str, Enum):
    admin = 'admin'
    partner = 'partner'
    operator = 'operator'