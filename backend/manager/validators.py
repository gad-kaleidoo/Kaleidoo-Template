from marshmallow import Schema, fields, validate

class ResourceSchema(Schema):
    """
    A generic schema for resource validation that can be customized for specific resource types.
    """
    name = fields.Str(required=True, validate=validate.Length(min=1),
                      error_messages={"required": "Name is required.",
                                      "validator_failed": "Name must not be empty."})
    description = fields.Str(required=False)
    type = fields.Str(required=True, validate=validate.OneOf(['type1', 'type2']),
                      error_messages={"required": "Type is required.",
                                      "validator_failed": "Invalid type. Must be 'type1' or 'type2'."})
    owner = fields.Str(required=True,
                       error_messages={"required": "Owner is required."})
    email = fields.Email(required=True, error_messages={"required": "Email is required.",
                                                        "invalid": "Invalid email format."})
    additional_info = fields.Dict(keys=fields.Str(), values=fields.Raw(), required=False)

class ResourceCreateSchema(ResourceSchema):
    """
    Schema for creating a new resource. Inherits the base ResourceSchema and adds/modifies fields specific to creation.
    """
    created_by = fields.Str(required=True, error_messages={"required": "Creator's user ID is required."})

class ResourceUpdateSchema(Schema):
    """
    Schema for updating an existing resource. Inherits the base ResourceSchema but makes all fields optional.
    """
    name = fields.Str(validate=validate.Length(min=1),
                      error_messages={"validator_failed": "Name must not be empty."})
    description = fields.Str(required=False)
    type = fields.Str(validate=validate.OneOf(['type1', 'type2']),
                      error_messages={"validator_failed": "Invalid type. Must be 'type1' or 'type2'."})
    owner = fields.Str()
    email = fields.Email(error_messages={"invalid": "Invalid email format."})
    additional_info = fields.Dict(keys=fields.Str(), values=fields.Raw(), required=False)
