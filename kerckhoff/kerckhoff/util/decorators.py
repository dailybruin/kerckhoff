from django.http import HttpRequest
from functools import wraps
from typing import List, Callable
from kerckhoff.exceptions import AuthenticationRequired

def api_login_required(methods : List[str]=["POST", "PUT", "PATCH", "DELETE"]):
    """Enforces user authentication for a particular endpoint

    Example:
        @api_login_required()
        def my_view(request):
            ...
    
    Keyword Arguments:
        methods {List[str]} -- The HTTP verbs that require authentication (default: {["POST", "PUT", "PATCH", "DELETE"]})
    
    Raises:
        AuthenticationRequired -- A KerckhoffCustomException that authentication is necessary
    
    Returns:
        the wrapped function
    """
    def decorator(function):
        @wraps(function)
        def wrap(request: HttpRequest, *args, **kwargs):
            if request.method in methods and not request.user.is_authenticated:
                raise AuthenticationRequired
            else request.user.is_authenticated:
                return function(request, *args, **kwargs)
        return wrap
    return decorator