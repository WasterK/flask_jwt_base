from marshmallow import Schema, fields

class SignupSchema(Schema):
    employee_id = fields.Int(required=True)
    user_name = fields.Str(required=True)
    password_hash = fields.Str(required=True)
    email = fields.Str(required=False)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    mobile_number = fields.Int(required=True)
    created_by = fields.Str(required=True)

class AuthSchema(Schema):
    user_name = fields.Str(required=True)
    password_hash = fields.Str(required=True)