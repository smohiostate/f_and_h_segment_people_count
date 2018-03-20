from inflection import camelize, underscore


def transform_values(item, transform):

    if type(item) is dict:
        transformed_dict = dict()
        for key in item:
            transformed_dict[transform(key)] = transform_values(item.get(key), transform)
        return transformed_dict

    elif type(item) is list:
        transformed_list = list()
        for list_item in item:
            transformed_list.append(transform_values(list_item, transform))
        return transformed_list

    else:
        return item


def transform_to_underscore(item):
    return transform_values(item, underscore)


def transform_to_camelcase(item, uppercase_first_letter=False):
    return transform_values(item, lambda v: camelize(v, uppercase_first_letter=uppercase_first_letter))
