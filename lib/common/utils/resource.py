from flask_restful import Resource
from common.utils.responses import forbidden, invalid_request
from common.utils.monitoring import get_logger

logger = get_logger(__name__)


class ResourceException(Exception):
    pass


class ResourceBase(Resource):

    @staticmethod
    def _catch_resource_exception(fn):
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except ResourceException as e:
                return invalid_request(message=e)
            except:
                raise
        return wrapper

    def get(self, *args, **kwargs):
        return self._catch_resource_exception(self.handle_get)(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self._catch_resource_exception(self.handle_post)(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self._catch_resource_exception(self.handle_put)(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return self._catch_resource_exception(self.handle_patch)(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._catch_resource_exception(self.handle_delete)(*args, **kwargs)

    # Override these methods
    def handle_get(self, *args, **kwargs):
        return forbidden()

    def handle_post(self, *args, **kwargs):
        return forbidden()

    def handle_put(self, *args, **kwargs):
        return forbidden()

    def handle_patch(self, *args, **kwargs):
        return forbidden()

    def handle_delete(self, *args, **kwargs):
        return forbidden()


class ResourceManager:
    """
        ResourceManager manages resources and provides
        a simple interface for hooking into and adding
        multiple resources tied to a module.
    """

    def __init__(self):
        self.resources = list()

    def resource(self, *urls, **kwargs):
        # This is a class decorator that is used to decorate
        # resource classes

        def cls_wrapper(cls):
            self.resources.append((cls, urls, kwargs))
            return cls

        return cls_wrapper

    def add_resource(self, resource, *urls, **kwargs):
        # Manually declare resources
        self.resources.append((resource, urls, kwargs))

    def attach_resources_to_api(self, api):
        number_of_resources = len(self.resources)
        logger.debug('Adding REST resources from this module, {} to add'.format(number_of_resources))

        for index, (resource, urls, kwargs) in enumerate(self.resources):
            logger.debug('Adding REST resource {} of {}'.format(index + 1, number_of_resources))
            api.add_resource(resource, *urls, **kwargs)
            logger.debug('Resource class {} will be bound to {}'.format(resource.__name__, ','.join(urls)))

        logger.debug('SUCCESS! %red%{} REST resources were added to the application successfully'.format(number_of_resources))

