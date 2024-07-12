from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404
from django.views import View

from ajax.forms import UserUpdateForm
from main.models import (Exercise,
                         Approach,
                         PowerTrainingExercise,
                         Cycling,
                         Swimming,
                         Walking,
                         Jogging,
                         PowerTraining,
                         Dish,
                         User)

SUCCESS_RESPONSE = JsonResponse({
    "status": "success",
}, status=200)

NOT_FOUND_RESPONSE = JsonResponse({
    "status": "error",
}, status=404)

INVALID_DATA_RESPONSE = JsonResponse({
    "status": "error",
}, status=422)


class UpdatePasswordView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> JsonResponse:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return JsonResponse({
                "status": "success",
            }, status=200)

        return JsonResponse({
            "status": "error",
            "errors": form.errors,
        }, status=422)


class UpdateUser(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> JsonResponse:
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return SUCCESS_RESPONSE

        return JsonResponse(
            {
                "status": "error",
                "errors": form.errors,
            }
        )


class AddPowerExerciseView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> JsonResponse:
        exercise_id = request.POST.get("exercise_id", default=None)
        training_id = request.POST.get("training_id", default=None)
        if not exercise_id or not training_id:
            return INVALID_DATA_RESPONSE

        try:
            exercise = Exercise.objects.get(pk=exercise_id)
        except Exercise.DoesNotExist:
            return NOT_FOUND_RESPONSE

        try:
            PowerTrainingExercise.objects.get(power_training_id=training_id,
                                              exercise_id=exercise_id)
            return INVALID_DATA_RESPONSE
        except PowerTrainingExercise.DoesNotExist:
            pass

        power_training = PowerTrainingExercise.objects.create(exercise=exercise,
                                                              power_training_id=training_id)
        return JsonResponse(
            {
                "status": "success",
                "power_training_id": power_training.id,
            }
        )


class AddApproachView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> JsonResponse:
        exercise_id = request.POST.get("power_training_exercise_id", default=None)
        weight = request.POST.get("weight", default=None)
        repeats = request.POST.get("repeats", default=None)

        if not exercise_id:
            return INVALID_DATA_RESPONSE

        if not repeats:
            return INVALID_DATA_RESPONSE

        try:
            power_exercise = PowerTrainingExercise.objects.get(pk=exercise_id)
        except (Exercise.DoesNotExist, Approach.DoesNotExist):
            return NOT_FOUND_RESPONSE

        approach = Approach(training_id=power_exercise.id,
                            repeats=repeats)
        if weight:
            approach.weight = weight

        approach.save()

        return SUCCESS_RESPONSE


class DeleteExerciseView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> JsonResponse:
        exercise_id = request.POST.get("exercise_id", default=None)

        if not exercise_id:
            return INVALID_DATA_RESPONSE

        get_object_or_404(PowerTrainingExercise, pk=exercise_id).delete()
        return SUCCESS_RESPONSE


class DeleteApproach(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> JsonResponse:
        approach_id = request.POST.get("approach_id", default=None)
        if not approach_id:
            return INVALID_DATA_RESPONSE

        get_object_or_404(Approach, id=approach_id).delete()
        return SUCCESS_RESPONSE


class DeleteTrainingView(LoginRequiredMixin, View):
    def post(self, request) -> JsonResponse:
        training_type = request.POST.get("type", default=None)
        training_id = request.POST.get("training_id", default=None)
        if not training_type or not training_id:
            return INVALID_DATA_RESPONSE

        if training_type == "PW":
            get_object_or_404(PowerTraining, pk=training_id).delete()
        elif training_type == "CY":
            get_object_or_404(Cycling, pk=training_id).delete()
        elif training_type == "SW":
            get_object_or_404(Swimming, pk=training_id).delete()
        elif training_type == "WK":
            get_object_or_404(Walking, pk=training_id).delete()
        elif training_type == "JG":
            get_object_or_404(Jogging, pk=training_id).delete()
        return SUCCESS_RESPONSE


class AddDishView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> JsonResponse:
        dish_id = request.POST.get("dish_id", default=None)
        meal_id = request.POST.get("meal_id", default=None)
        weight = request.POST.get("weight", default=None)

        if not dish_id:
            return INVALID_DATA_RESPONSE

        try:
            dish = User.dishes.get(pk=dish_id)
        except Dish.DoesNotExist:
            return NOT_FOUND_RESPONSE


