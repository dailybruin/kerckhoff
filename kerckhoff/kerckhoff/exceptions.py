class KerckhoffCustomException(Exception):
    status_code = None
    error_message = None
    is_an_error_response = True
    def __init__(self, error_message):
        Exception.__init__(self)
        self.error_message = error_message
    def to_dict(self):
        return {'message': self.error_message}

class UserError(KerckhoffCustomException):
    status_code = 400