from enum import Enum


class CarCategory(str, Enum):
    EURO3 = "EURO3"
    EURO4 = "EURO4"
    EURO5 = "EURO5"
    EURO6 = "EURO6"
    HYBRID = "HYBRID"
    ELECTRIC = "ELECTRIC"
