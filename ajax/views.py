from rest_framework import mixins
from rest_framework.generics import DestroyAPIView
from rest_framework.viewsets import GenericViewSet

from ajax.serializers import CreateDishCountSerializer
from main.models import (
    Dish,
    DishCount,
    Exercise,
    Meal,
)
from permissions import (
    IsAuthenticatedAndOwnerPermission,
    IsAuthenticatedAndDishCountOwner
)


class DishCountViewSet(
    GenericViewSet,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
):
    queryset = DishCount.objects.all()
    permission_classes = (IsAuthenticatedAndDishCountOwner,)
    serializer_class = CreateDishCountSerializer


class DeleteExerciseView(DestroyAPIView):
    queryset = Exercise.objects.all()
    permission_classes = (IsAuthenticatedAndOwnerPermission,)


class DeleteDishView(DestroyAPIView):
    queryset = Dish.objects.all()
    permission_classes = (IsAuthenticatedAndOwnerPermission,)


class DeleteMealView(DestroyAPIView):
    queryset = Meal.objects.all()
    permission_classes = (IsAuthenticatedAndOwnerPermission,)
