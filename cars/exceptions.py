from rest_framework.exceptions import APIException


class BadRequest(APIException):
    status_code = 400
    default_detail = 'Data in wrong format'
    default_code = 'BAD REQUEST'


class NotFound(APIException):
    status_code = 404
    default_detail = 'Car does not exist'
    default_code = 'NOT FOUND'
