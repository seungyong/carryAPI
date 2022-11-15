from typing import List


def to_decimal_place_cut(decimal: float | str, precision: int) -> str:
    if type(decimal) == float:
        value: str = str(decimal)
    else:
        value = decimal

    find_decimal_places: List[str] = value.split('.')
    cut_decimal: str = str(find_decimal_places[0] + '.' + find_decimal_places[1][:precision])

    return cut_decimal
