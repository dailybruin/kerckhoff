from django.http import JsonResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import logging
import traceback

logger = logging.getLogger(settings.APP_NAME)

def is_registered(exception: Exception):
    try:
        return exception.is_an_error_response
    except AttributeError:
        return False

class RequestExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if is_registered(exception):
            status = exception.status_code
            exception_dict = exception.to_dict()
        else:
            status = 500
            exception_dict = {'message': 'Unexpected server error'}
            logger.error("ERROR 500 - %s" %  traceback.format_exc())
            if settings.DEBUG:
                raise exception

        return JsonResponse(exception_dict, status=status)
