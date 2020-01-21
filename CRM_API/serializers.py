import os

from django.conf import settings
from rest_framework import serializers
from CRM_API.models import Customer


class CustomerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'surname', 'img_url')


# Delete a customer's previous image if it isn't the default image.
def delete_previous_image(customer):
    if str(customer.img_url) != settings.DEFAULT_IMAGE_FILE:
        path_to_delete = (settings.MEDIA_ROOT + '/' + str(customer.img_url))
        if os.path.exists(path_to_delete):
            os.remove(path_to_delete)


class CustomerCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)

        # Update the image only if requested.
        if instance.img_url != str(validated_data.get('img_url')):
            delete_previous_image(instance)

            instance.img_url = validated_data.get('img_url')

        instance.last_updated_by_id = validated_data.get('last_updated_by', instance.last_updated_by_id)
        instance.save()
        return instance
