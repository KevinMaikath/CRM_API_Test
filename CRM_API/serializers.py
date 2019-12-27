from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from CRM_API.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        # extra_kwargs = {
        #     'created_by': {'write_only': True},
        #     'last_updated_by': {'write_only': True}
        # }


    def update(self, instance, validated_data):
        print(instance.last_updated_by_id)
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.imgUrl = validated_data.get('imgUrl', instance.imgUrl)
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
