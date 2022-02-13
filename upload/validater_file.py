from tabnanny import check
from django.core.exceptions import ValidationError

# check if file size is greater than 100MB
def validate_file(file):
    if file.size > (100 * 1024 * 1024):
        raise ValidationError("The maximum file size that can be uploaded is 100MB")
    else:
        return file