from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    class Meta:
        model = get_user_model()
        fields = ['username', 'email','first_name', 'last_name', 'password']

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    username = serializers.CharField(min_length=3)
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, min_length=6)
    new_password = serializers.CharField(required=True, min_length=6)


class UpdateUserProfileSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']

    def update(self, instance, validated_data):
        #bulk update the only fields that are supplied using the key
        for key in validated_data.keys():
            setattr(instance, key, validated_data[key])
        instance.save()
        print(instance.username)
        return instance
