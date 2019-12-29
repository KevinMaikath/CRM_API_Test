from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


# Creates an url with the project's setting values, formatting the image to the project's default image format.
def custom_upload_path(instance, filename):
    file_str = str(filename)
    dot = file_str.index('.')
    file_str = file_str[:dot+1]

    return f'{settings.IMAGE_FOLDER}{file_str}{settings.IMAGE_FORMAT}'


class Customer(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    img_url = models.ImageField(upload_to=custom_upload_path, max_length=100,
                                default=settings.IMAGE_FOLDER + settings.DEFAULT_IMAGE_FILE)

    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='customer_created_by')
    last_updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='customer_last_updated_by')

    # Simple 'toString', for debug purposes.
    def __str__(self):
        return f'Customer: {self.surname}, {self.name}'

    # Crop the image if necessary.
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.img_url.path)

        if img.height > settings.IMAGE_MAX_HEIGHT or img.width > settings.IMAGE_MAX_WIDTH:
            output_size = (settings.IMAGE_MAX_HEIGHT, settings.IMAGE_MAX_WIDTH)
            img.thumbnail(output_size)
            img.save(self.img_url.path)
