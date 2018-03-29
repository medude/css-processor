from enum import Enum


class States(Enum):
    INITIAL = 0
    RULE = 1
    DIRECTIVE = 2
    VARIABLE = 3
    CONSTANT = 4
