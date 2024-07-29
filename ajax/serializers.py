from django.contrib.auth import get_user_model
from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs.get('new_password1') != attrs.get('new_password2'):
            raise serializers.ValidationError(
                {
                    'new_password2': 'Passwords do not match!'
                }
            )
        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "birth_date",
            "weight",
            "height",
            "sex"
        )
