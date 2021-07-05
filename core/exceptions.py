from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError

from core.error_codes import SERVICE_ERROR, BAD_REQUEST, DATA_VALIDATION, OUT_OF_STOCK, RESERVATION_CANCELLED


class InternalServiceError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = {
        'error': {
            'type': SERVICE_ERROR,
            'message': 'A server error occurred.'
        }
    }
    default_code = 'error'


class BadRequestError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    default_detail = {
        'error': {
            'type': BAD_REQUEST,
            'message': 'Invalid request sent'
        }
    }


class SerializerError(ValidationError):
    detail = {
        'error': {
            'type': DATA_VALIDATION,
            'message': None
        }
    }

    def __init__(self, serializer_error_message):
        self.detail['error']['message'] = serializer_error_message


class OutOfStockError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    default_detail = {
        'error': {
            'type': OUT_OF_STOCK,
            'message': 'No tickets left'
        }
    }


class ReservationCancelledError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    default_detail = {
        'error': {
            'type': RESERVATION_CANCELLED,
            'message': 'Reservation was already cancelled'
        }
    }
