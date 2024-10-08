# auth/schemas.py
from marshmallow import Schema, fields

class AuthSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

