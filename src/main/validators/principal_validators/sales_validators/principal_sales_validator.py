from cerberus import Validator

from src.exceptions.api_types import ValidationFailed

class PrincipalSalesValidator:


    @staticmethod
    def validate(request: any) -> None:
        schema = {
            'ibm': {
                'type': 'list',
                'schema': {'type': 'string', 'empty': False},
                'minlength': 1,
                'required': True
            },
            'data': {
                'type': 'string',
                'regex': r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$',
                'required': True
            },
            'rede': {
                'type': 'list',
                'schema': {'type': 'string', 'empty': False},
                'minlength': 1,
                'required': True
            }
        }

        v = Validator(schema)
        try:
            body =  request.json
        except Exception as e:
            raise ValidationFailed("Request body must be a valid JSON.")

        if not v.validate(body):
            raise ValidationFailed(f"Invalid request data: {v.errors}")