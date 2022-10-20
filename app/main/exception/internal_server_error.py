from flask import request
from flask_restx import fields

from app.main.util.constants import *


class InternalServerError(Exception):
    def __init__(self, message):
        self.error = INTERNAL_SERVER_ERROR['error']
        self.code = INTERNAL_SERVER_ERROR['code']
        self.message = message
        self.path = request.path

        super().__init__(message)

    def __str__(self):
        return self.message

    @staticmethod
    def response_model():
        return {
            'error': fields.String(INTERNAL_SERVER_ERROR['error']),
            'code': fields.Integer(INTERNAL_SERVER_ERROR['code']),
            'message': fields.String('Error Message'),
            'path': fields.String('Request URL')
        }
