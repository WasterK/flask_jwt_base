from marshmallow import Schema, fields, validate

class DeviceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    interface_type = fields.Str(required=True, validate=validate.OneOf(['modbus', 'pulse']))
    status = fields.Str(required=True, validate=validate.OneOf(['active', 'inactive']))
