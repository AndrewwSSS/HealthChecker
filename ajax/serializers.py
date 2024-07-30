from django.contrib.auth import get_user_model
from rest_framework import serializers

from main.models import (
    Approach,
    DishCount,
    PowerTrainingExercise,
)


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


class PeriodSerializer(serializers.Serializer):
    period = serializers.CharField(max_length=10)

    def validate(self, attrs):
        period = attrs.get("period")
        if not period:
            raise serializers.ValidationError()
        if period.lower() not in ("today", "this month", "this year"):
            raise serializers.ValidationError(
                {"period": "Invalid period!"}
            )
        attrs["period"] = period.lower()
        return attrs


class CreatePowerTrainingExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerTrainingExercise
        fields = ("id", "exercise", "power_training")


class ApproachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approach
        fields = (
            "id",
            "weight",
            "repeats",
            "training"
        )


class CreateDishCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishCount
        fields = [
            "id",
            "dish",
            "weight",
            "meal"
        ]


class UpdateDishCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishCount
        fields = [
            "id",
            "weight"
        ]