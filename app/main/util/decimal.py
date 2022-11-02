def to_first_decimal_place_cut(decimal):
    if type(decimal) == float:
        value = str(decimal)

    find_decimal_places = value.split('.')
    cut_first_decimal = float(str(find_decimal_places[0] + '.' + find_decimal_places[1][:1]))

    return cut_first_decimal
