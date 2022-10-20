from flask import request
from flask_restx import fields

from app.main.util.constants import *


class Forbidden(Exception):
    def __init__(self, message):
        self.error = FORBIDDEN['error']
        self.code = FORBIDDEN['code']
        self.message = message
        self.path = request.path

        super().__init__(message)

    def __str__(self):
        return self.message

    @staticmethod
    def response_model():
        return {
            'error': fields.String(FORBIDDEN['error']),
            'code': fields.Integer(FORBIDDEN['code']),
            'message': fields.String("You can't access this url or not found url"),
            'path': fields.String('Request URL')
        }
