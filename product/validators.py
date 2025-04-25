from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_size =10
    max_size_in_bytes = max_size * 1024 * 1024  # 10 MB in bytes
    if file.size > max_size_in_bytes:
        raise ValidationError(f"File size exceeds the limit of {max_size} KB.")
