from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from ajax.forms import UserUpdateForm
from main.models import (Exercise,
                         Approach,
                         PowerTrainingExercise, Training, CyclingTraining, SwimmingTraining, Walk, Jogging)

INVALID_METHOD_RESPONSE = JsonResponse(
    {
        "status": "error"
    },
    status=405
)

SUCCESS_RESPONSE = JsonResponse({
    "status": "success",
}, status=200)

NOT_FOUND_RESPONSE = JsonResponse({
    "status": "error",
}, status=404)

INVALID_DATA_RESPONSE = JsonResponse({
    "status": "error",
}, status=422)


@login_required
def change_password(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse(
            {
                "status": "Method not allowed"
            },
            status=405
        )

    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return JsonResponse({
            "status": "success",
        }, status=200)

    return JsonResponse(
        {
            "status": "error",
            "errors": form.errors,
        }, status=422
    )


@login_required
def update_user(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return INVALID_METHOD_RESPONSE

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


@login_required
def add_power_exercise(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return INVALID_METHOD_RESPONSE

    exercise_id = request.POST.get("exercise_id", default=None)
    training_id = request.POST.get("training_id", default=None)
    if not exercise_id or not training_id:
        return INVALID_DATA_RESPONSE

    try:
        exercise = Exercise.objects.get(pk=exercise_id)
    except Exercise.DoesNotExist:
        return NOT_FOUND_RESPONSE

    try:
        PowerTrainingExercise.objects.get(power_training_id=training_id, exercise_id=exercise_id)
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


@login_required
def add_approach(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return INVALID_METHOD_RESPONSE

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


@login_required
def delete_exercise(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return INVALID_METHOD_RESPONSE

    exercise_id = request.POST.get("exercise_id", default=None)

    if not exercise_id:
        return INVALID_DATA_RESPONSE

    try:
        exercise = PowerTrainingExercise.objects.get(pk=exercise_id)
        exercise.delete()
        return SUCCESS_RESPONSE
    except Exercise.DoesNotExist:
        return NOT_FOUND_RESPONSE


def delete_approach(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return INVALID_METHOD_RESPONSE

    approach_id = request.POST.get("approach_id", default=None)
    if not approach_id:
        return INVALID_DATA_RESPONSE

    try:
        approach = Approach.objects.get(pk=approach_id)
        approach.delete()
        return SUCCESS_RESPONSE
    except Approach.DoesNotExist:
        return NOT_FOUND_RESPONSE


def delete_training(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return INVALID_METHOD_RESPONSE

    training_type = request.POST.get("type", default=None)
    training_id = request.POST.get("training_id", default=None)
    if not training_type or not training_id:
        return INVALID_DATA_RESPONSE

    try:
        if training_type == "PW":
            training = PowerTrainingExercise.objects.get(pk=training_id)
            training.delete()
        elif training_type == "CY":
            training = CyclingTraining.objects.get(pk=training_id)
            training.delete()
        elif training_type == "SW":
            training = SwimmingTraining.objects.get(pk=training_id)
            training.delete()
        elif training_type == "WK":
            training = Walk.objects.get(pk=training_id)
            training.delete()
        elif training_type == "JG":
            training = Jogging.objects.get(pk=training_id)
            training.delete()
        return SUCCESS_RESPONSE
    except Exception:
        return INVALID_DATA_RESPONSE


def change_power_training_exercise(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return INVALID_METHOD_RESPONSE
    #todo