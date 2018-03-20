from common.utils.string_manipulation import transform_to_camelcase

def standard_response(response=None, metaquery=None, status_text='', status_code=400):
    response = {} if response is None else response
    response['status_text'] = status_text
    response['status'] = status_code

    if metaquery is not None and type(metaquery) is dict:
        response['metaquery'] = metaquery

    return transform_to_camelcase(response), status_code


def ok(response=None, message='OK', metaquery=None):
    # OK - GET
    # The Consumer requested data from the Server, and the Server found it for them (Idempotent)
    return standard_response(response, metaquery=metaquery, status_text=message, status_code=200)


def created(response=None, message='Created', metaquery=None):
    # CREATED - POST
    # The Consumer gave the Server data, and the Server created a resource
    return standard_response(response, metaquery=metaquery, status_text=message, status_code=201)


def no_content():
    # NO CONTENT - PUT/PATCH/DELETE
    # The Consumer asked the Server to update a Resource, and the Server updated it
    return standard_response({}, metaquery=None, status_text='', status_code=204)


def invalid_request(response=None, message='Invalid Request', metaquery=None):
    # INVALID_REQUEST - POST/PUT/PATCH
    # The Consumer gave bad data to the Server, and the Server did nothing with it (Idempotent)
    return standard_response(response, metaquery=metaquery, status_text=message, status_code=400)


def unauthorized(response=None, message='Unauthorized', metaquery=None):
    return standard_response(response, metaquery=metaquery, status_text=message, status_code=401)


def forbidden(response=None, message='Forbidden', metaquery=None):
    return standard_response(response, metaquery=metaquery, status_text=message, status_code=403)


def not_found(response=None, message='Not Found', metaquery=None):
    # NOT FOUND - *
    # The Consumer referenced an non-existent Resource or Collection, and the Server did nothing (Idempotent)
    return standard_response(response, metaquery=metaquery, status_text=message, status_code=404)
