import os

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from CRM_API.models import Customer


class CustomerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'surname', 'img_url')


class CustomerCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)

        # Update the image only if requested.
        if instance.img_url != settings.IMAGE_FOLDER + str(validated_data.get('img_url')):

            # Delete the previous one if it isn't the default image.
            if str(instance.img_url) != settings.IMAGE_FOLDER + settings.DEFAULT_IMAGE_FILE:
                path_to_delete = (settings.MEDIA_ROOT + '/' + str(instance.img_url))
                if os.path.exists(path_to_delete):
                    os.remove(path_to_delete)

            instance.img_url = validated_data.get('img_url')

        instance.last_updated_by_id = validated_data.get('last_updated_by', instance.last_updated_by_id)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
