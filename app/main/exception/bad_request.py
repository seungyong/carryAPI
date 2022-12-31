from flask import request
from flask_restx import fields

from app.main.util.constants import *


class BadRequest(Exception):
    def __init__(self, message):
        self.error = BAD_REQUEST['error']
        self.code = BAD_REQUEST['code']
        self.message = message
        self.path = request.path

        super().__init__(message)

    def __str__(self):
        return self.message

    @staticmethod
    def response_model():
        return {
            'error': fields.String(BAD_REQUEST['error']),
            'code': fields.Integer(BAD_REQUEST['code']),
            'message': fields.String('Bad Request Parameters'),
            'path': fields.String('Request URL')
        }
