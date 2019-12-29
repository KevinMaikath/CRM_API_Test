from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)

    # Currently use URL as image. It can be later migrated to an image file.
    img_url = models.TextField()

    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='customer_created_by')
    last_updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='customer_last_updated_by')

    # Simple 'toString', for debug purposes.
    def __str__(self):
        return f'Customer: {self.surname}, {self.name}'
