from PIL import Image
from django.contrib.auth.models import User
from django.db import models


def custom_upload_path(instance, filename):
    return f'images/{instance.name}_image.png'


class Customer(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    img_url = models.ImageField(upload_to=custom_upload_path, max_length=100)

    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='customer_created_by')
    last_updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='customer_last_updated_by')

    # Simple 'toString', for debug purposes.
    def __str__(self):
        return f'Customer: {self.surname}, {self.name}'

    # Crop the image to maximum 300x300
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.img_url.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.img_url.path)
