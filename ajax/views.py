from rest_framework import mixins
from rest_framework import status
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ajax.serializers import DishCountSerializer
from ajax.serializers import MealSerializer
from main.models import (
    Dish,
    DishCount,
    Exercise,
    Meal,
)
from permissions import (
    IsAuthenticatedAndDishCountOwner,
    IsAuthenticatedAndOwnerPermission,
)


class DishCountViewSet(
    GenericViewSet,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
):
    queryset = DishCount.objects.all()
    permission_classes = (IsAuthenticatedAndDishCountOwner,)
    serializer_class = DishCountSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        meal_data = self.perform_destroy(instance)
        return Response(
            meal_data,
            status=status.HTTP_200_OK
        )

    def perform_destroy(self, instance):
        related_meal = instance.meal

        instance.delete()

        meal_data = MealSerializer(related_meal).data

        return meal_data


class DeleteExerciseView(DestroyAPIView):
    queryset = Exercise.objects.all()
    permission_classes = (IsAuthenticatedAndOwnerPermission,)


class DeleteDishView(DestroyAPIView):
    queryset = Dish.objects.all()
    permission_classes = (IsAuthenticatedAndOwnerPermission,)


class MealViewSet(
    GenericViewSet,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = Meal.objects.all()
    permission_classes = (IsAuthenticatedAndOwnerPermission,)
    serializer_class = MealSerializer
