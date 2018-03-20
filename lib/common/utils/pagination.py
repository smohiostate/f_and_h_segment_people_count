# Pagination constants
LIMIT_DEFAULT = 25
OFFSET_DEFAULT = 0
ORDER_DEFAULT = 'asc'

from functools import wraps
from flask_restful import reqparse

def paginate(fn):
    """
        paginate() will parse the request and add two arguments to the
        decorated function: limit, offset
        :param fn: The target function
        :return: A decorated function with two arguments injected
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        pagination = get_pagination()
        limit = pagination.limit if pagination.limit is not None else LIMIT_DEFAULT
        offset = pagination.offset if pagination.offset is not None else OFFSET_DEFAULT

        return fn(*args, limit=limit, offset=offset, **kwargs)

    return wrapper


def get_pagination():
    parser = reqparse.RequestParser()
    parser.add_argument('limit', type=int, help="Invalid input for limit parameter.")
    parser.add_argument('offset', type=int, help="Invalid input for offset parameter.")
    return parser.parse_args()


def generate_metaquery(result_count=None, total_count=None, limit=LIMIT_DEFAULT, offset=OFFSET_DEFAULT,
                  next_result=None, previous_result=None):
    metaquery = {'result_count': result_count, 'total_count': total_count,
            'limit': limit, 'offset': offset}

    if next_result is not None:
        metaquery['next_result'] = next_result

    if previous_result is not None:
        metaquery['previous_result'] = previous_result

    return metaquery
