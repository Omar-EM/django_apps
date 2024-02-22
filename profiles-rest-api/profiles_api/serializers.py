from rest_framework import serializers

from . import models

# Serializers are very similar to django forms
class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing out APIView"""
    name = serializers.CharField(max_length=10)


class UserPorfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    # See docs:
    # https://www.django-rest-framework.org/api-guide/serializers/#modelserializer

    class Meta:     # Used to configure the serializer
        model = models.UserProfile
        # List of fields that we want to be accessible
        fields = ('id', 'email', 'name', 'password')
        # The extra_kwargs is used to set the password field to read_only & to a password field (****)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    # By default, it uses the create method provided by the object manager to create the object
    # We want to override it, so that we use the create_user() that we defined so that we store the hash of the pwd
    def create(self, validated_data):
        """Create and return a new user
            Called when using POST
        """
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """Handle updating user account
            Called when using PUT/PATCH?
        """
        # Same as create(), we override it to store hashed pwd, instead of plain text
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serizalizes a profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {
            'user_profiles': {'read_only': True}
        }

