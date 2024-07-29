from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View, generic
from rest_framework.generics import CreateAPIView, DestroyAPIView

from ajax.forms import ApproachForm
from ajax.serializers import ApproachSerializer, CreatePowerTrainingExerciseSerializer
from ajax.views import INVALID_DATA_RESPONSE, SUCCESS_RESPONSE
from main.models import (
    Approach,
    Cycling,
    Jogging,
    PowerTraining,
    PowerTrainingExercise,
    Swimming,
    Walking,
)
from permissions import (
    IsAuthenticatedAndApproachOwner,
    IsAuthenticatedAndOwnerPermission,
    IsAuthenticatedAndPowerTrainingExerciseOwner,
)


class CreatePowerExerciseView(CreateAPIView):
    queryset = PowerTrainingExercise.objects.all()
    serializer_class = CreatePowerTrainingExerciseSerializer
    permission_classes = (IsAuthenticatedAndPowerTrainingExerciseOwner,)


class CreateApproachView(CreateAPIView):
    queryset = Approach.objects.all()
    serializer_class = ApproachSerializer
    permission_classes = (IsAuthenticatedAndApproachOwner,)


class DeletePowerTrainingExerciseView(DestroyAPIView):
    queryset = PowerTrainingExercise.objects.all()
    serializer_class = CreatePowerTrainingExerciseSerializer
    permission_classes = (IsAuthenticatedAndPowerTrainingExerciseOwner,)


class DeleteApproachView(DestroyAPIView):
    queryset = Approach.objects.all()
    serializer_class = ApproachSerializer
    permission_classes = (IsAuthenticatedAndApproachOwner,)


class DeleteTraining(DestroyAPIView):
    permission_classes = (IsAuthenticatedAndOwnerPermission,)


class DeletePowerTraining(DeleteTraining):
    queryset = PowerTraining.objects.all()


class DeleteCycling(DeleteTraining):
    queryset = Cycling.objects.all()


class DeleteSwimming(DeleteTraining):
    queryset = Swimming.objects.all()


class DeleteJogging(DeleteTraining):
    queryset = Jogging.objects.all()


class DeleteWalking(DeleteTraining):
    queryset = Walking.objects.all()
