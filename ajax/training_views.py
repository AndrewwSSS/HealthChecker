from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views import generic

from ajax.forms import ApproachForm
from ajax.forms import PowerExerciseForm
from ajax.views import INVALID_DATA_RESPONSE
from ajax.views import SUCCESS_RESPONSE
from main.models import Approach
from main.models import Cycling
from main.models import Exercise
from main.models import Jogging
from main.models import PowerTraining
from main.models import PowerTrainingExercise
from main.models import Swimming
from main.models import Walking


class CreatePowerExerciseView(LoginRequiredMixin, View):
    form_class = PowerExerciseForm
    model = PowerTrainingExercise

    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        exercise_id = request.POST.get("exercise", default=None)
        training_id = request.POST.get("training", default=None)

        if not exercise_id or not training_id:
            return INVALID_DATA_RESPONSE

        exercise = get_object_or_404(Exercise, pk=exercise_id)
        power_training = get_object_or_404(
            PowerTraining,
            pk=training_id,
            user=request.user
        )

        # Check if exercise with same name exists
        if power_training.exercises.filter(exercise_id=exercise.id).exists():
            return INVALID_DATA_RESPONSE

        power_training_exercise = PowerTrainingExercise.objects.create(
            exercise=exercise,
            power_training_id=training_id
        )
        return JsonResponse(
            {
                "status": "success",
                "id": power_training_exercise.id,
            }
        )


class CreateApproachView(LoginRequiredMixin, generic.CreateView):
    model = Approach
    form_class = ApproachForm

    def form_valid(self, form):
        approach = form.save(commit=False)

        get_object_or_404(
            PowerTrainingExercise,
            pk=approach.training.id,
            power_training__user=self.request.user,
        )
        approach.save()
        return JsonResponse({"id": approach.id}, status=200)


class DeletePowerExerciseView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        exercise_id = request.POST.get("exercise", default=None)

        if not exercise_id:
            return INVALID_DATA_RESPONSE

        get_object_or_404(
            PowerTrainingExercise,
            pk=exercise_id,
            power_training__user=request.user
        ).delete()
        return SUCCESS_RESPONSE


class DeleteApproach(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        approach = request.POST.get("approach", default=None)
        exercise = request.POST.get("exercise", default=None)

        if not approach or not exercise:
            return INVALID_DATA_RESPONSE

        get_object_or_404(
            Approach,
            id=approach,
            training__power_training__user_id=request.user.id,
            training_id=exercise,
        ).delete()
        return SUCCESS_RESPONSE


class DeleteTrainingView(LoginRequiredMixin, View):
    @staticmethod
    def post(request) -> JsonResponse:
        training_type = request.POST.get("type", default=None)
        training_id = request.POST.get("id", default=None)
        if not training_type or not training_id:
            return INVALID_DATA_RESPONSE

        training_class = None
        if training_type == "PW":
            training_class = PowerTraining
        elif training_type == "CY":
            training_class = Cycling
        elif training_type == "SW":
            training_class = Swimming
        elif training_type == "WK":
            training_class = Walking
        elif training_type == "JG":
            training_class = Jogging
        else:
            return INVALID_DATA_RESPONSE
        get_object_or_404(
            training_class,
            pk=training_id,
            user=request.user).delete()
        return SUCCESS_RESPONSE
