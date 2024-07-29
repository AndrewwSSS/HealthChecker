from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from ajax.forms import ApproachForm, DishCountForm
from main.models import (
    Approach,
    Dish,
    DishCount,
    Exercise,
    Meal,
)

SUCCESS_RESPONSE = JsonResponse(
    {
        "status": "Success",
    },
    status=200,
)

INVALID_DATA_RESPONSE = JsonResponse(
    {
        "status": "error",
    },
    status=422,
)


class CreateDishCountView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        form = DishCountForm(request.POST, user=request.user)
        if form.is_valid():
            dish_count = form.save()
            return JsonResponse(
                {
                    "id": dish_count.id,
                },
                status=200,
            )
        else:
            return INVALID_DATA_RESPONSE


class UpdateDishCountView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        dish_count_id = request.POST.get("dish_count", default=None)
        weight = request.POST.get("weight", default=None)

        if not dish_count_id or not weight:
            return INVALID_DATA_RESPONSE

        with transaction.atomic():
            dish_count_queryset = DishCount.objects.select_for_update().filter(
                id=dish_count_id
            )
            if not dish_count_queryset.exists():
                return INVALID_DATA_RESPONSE

            dish_count = dish_count_queryset.first()

            if dish_count.meal.user != request.user:
                return INVALID_DATA_RESPONSE

            dish_count.weight = weight
            dish_count.save()
            return SUCCESS_RESPONSE


class DeleteDishCountView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        dish_count_id = request.POST.get("dish_count", default=None)
        if not dish_count_id:
            return INVALID_DATA_RESPONSE

        with transaction.atomic():
            dish_count_queryset = DishCount.objects.select_for_update().filter(
                id=dish_count_id
            )
            if not dish_count_queryset.exists():
                return INVALID_DATA_RESPONSE

            dish_count = dish_count_queryset.first()
            if dish_count.meal.user != request.user:
                return INVALID_DATA_RESPONSE
            dish_count.delete()
            return SUCCESS_RESPONSE


class UpdateApproachView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        approach_id = request.POST.get("id", default=None)
        if not approach_id:
            return INVALID_DATA_RESPONSE
        with transaction.atomic():
            approach_queryset = (Approach.objects.select_for_update()
                                 .filter(id=approach_id))
            if not approach_queryset.exists():
                return INVALID_DATA_RESPONSE
            approach = approach_queryset.first()

            form = ApproachForm(request.POST, instance=approach)
            if form.is_valid():
                approach = form.save(commit=False)
                if approach.training.power_training.user != request.user:
                    return INVALID_DATA_RESPONSE
                approach.save()
                return SUCCESS_RESPONSE
            else:
                return INVALID_DATA_RESPONSE


class DeleteExerciseView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        exercise_id = request.POST.get("exercise_id", default=None)

        if not exercise_id:
            return INVALID_DATA_RESPONSE

        get_object_or_404(
            Exercise,
            id=exercise_id,
            user=request.user
        ).delete()
        return SUCCESS_RESPONSE


class DeleteDishView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        dish_id = request.POST.get("id", default=None)
        if not dish_id:
            return INVALID_DATA_RESPONSE
        get_object_or_404(
            Dish,
            id=dish_id,
            user=request.user
        ).delete()
        return SUCCESS_RESPONSE


class DeleteMealView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        meal_id = request.POST.get("id", default=None)
        if not meal_id:
            return INVALID_DATA_RESPONSE
        get_object_or_404(
            Meal,
            id=meal_id,
            user=request.user
        ).delete()
        return SUCCESS_RESPONSE



