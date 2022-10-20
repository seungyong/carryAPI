from flask import request
from flask_restx import fields

from app.main.util.constants import *


class DataNotFound(Exception):
    def __init__(self, message):
        self.error = NOT_FOUND['error']
        self.code = NOT_FOUND['code']
        self.message = message
        self.path = request.path

        super().__init__(message)

    def __str__(self):
        return self.message

    @staticmethod
    def response_model():
        return {
            'error': fields.String(NOT_FOUND['error']),
            'code': fields.Integer(NOT_FOUND['code']),
            'message': fields.String('Error Message'),
            'path': fields.String('Request URL')
        }
