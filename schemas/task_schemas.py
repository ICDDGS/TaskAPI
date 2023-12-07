from marshmallow import fields, validates, ValidationError
from datetime import datetime
import re
class TaskSchema:
    """
    Class that defines schema for individual tasks.
    """
    _id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False)
    due = fields.Str(required=True)
    status = fields.Str(required=True)

    @validates('due')
    def validate_due(self, value):
        """
        Validates the duename date format.

        Args:
            value: The due date string.

        Raises:
            ValidationError: If the due date does not have the format "YYYY-MM-DD HH:mm:ss".
        """
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValidationError('Due date must have the format "YYYY-MM-DD HH:mm:ss".')

    @validates('status')
    def validate_status(self, value):
        """
        Validates the task status.

        Args:
            value: The task status.

        Raises:
            ValidationError: If the status is not "Complete" or "Pending".
        """
        if value not in ['Complete', 'Pending']:
            raise ValidationError('Status must be Complete or Pending.')

