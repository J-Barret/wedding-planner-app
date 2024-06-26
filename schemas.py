from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
	id = fields.Int(dump_only=True)
	name = fields.Str(required=True)
	password = fields.Str(required=True, load_only=True)





