from marshmallow import fields, validates, ValidationError

class BookSchema:
    title = fields.String(required=True)
    author = fields.String(required=True)

    @validates('title')
    def validate_title(self, value):
        if len(value) < 5:
            raise ValidationError('Title must be at leat 5 characters long.')
        
    @validates('author')
    def validate_author(self, value):
        if len(value) < 5:
            raise ValidationError('Author must be at leat 5 characters long.')