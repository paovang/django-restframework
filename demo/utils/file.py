from django.core.exceptions import ValidationError
# from drf_orm.settings import FILE_UPLOAD_MAX_MEMORY_SIZE
# from rest_framework import serializers
# from PIL import Image
# from io import BytesIO
import os


def validate_image_extension(image):
    allowed_extensions = ['jpeg', 'jpg', 'png', 'gif']
    extension = image.name.split('.')[-1].lower()

    if extension not in allowed_extensions:
        raise ValidationError(
            "Invalid image format. Please upload a valid image file (JPG, JPEG, PNG, GIF)."
        )

def custom_cover_image_filename(instance, filename):
    # Modify the file name as needed
    com_user_id = instance.id  # Assuming your Book model has an 'id' field
    if com_user_id is None:
        # If the book is new and doesn't have an ID yet, use a temporary identifier
        com_user_id = "new_user"
    ext = filename.split('.')[-1]  # Get the file extension
    new_filename = f'com_user_{com_user_id}.{ext}'  # Customize the new file name
    return os.path.join('company/users/', new_filename)