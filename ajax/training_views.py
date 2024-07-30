from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from rest_framework.viewsets import GenericViewSet

from ajax.serializers import (
    ApproachSerializer,
    CreatePowerTrainingExerciseSerializer,
)
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


class ApproachViewSet(
    GenericViewSet,
    DestroyAPIView,
    UpdateAPIView,
    CreateAPIView,
):
    queryset = Approach.objects.all()
    serializer_class = ApproachSerializer
    permission_classes = (IsAuthenticatedAndApproachOwner,)


class DeletePowerTrainingExerciseView(DestroyAPIView):
    queryset = PowerTrainingExercise.objects.all()
    permission_classes = (IsAuthenticatedAndPowerTrainingExerciseOwner,)


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
