def convert_to_type(item, to_type, value_on_type_error):
    try:
        return to_type(item)
    except ValueError:
        return value_on_type_error


def parse_bounding_box(x_top, y_top, x_bottom, y_bottom):
    width = x_bottom - x_top
    height = y_bottom - y_top
    return x_top, y_top, width, height


def get_maximum_value(iterable, getter=lambda item: item):
    if len(iterable) == 0:
        return None

    maximum = getter(iterable[0])

    for classification in iterable[1:]:
        maximum = max(maximum, getter(classification))

    return maximum
