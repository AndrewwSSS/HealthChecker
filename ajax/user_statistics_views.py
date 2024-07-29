from datetime import date

from django.db.models import Q, QuerySet
from django.db.models.functions import TruncDate
from django.http import HttpRequest
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ajax.serializers import PeriodSerializer
from ajax.services import UserStatisticService
from main.models import (
    Cycling,
    Jogging,
    Meal,
    Swimming,
    Training,
    User,
    Walking,
)


class GetTrainingsTypeRatioView(GenericAPIView):
    serializer_class = PeriodSerializer

    def get(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        service = UserStatisticService(request.user)
        return Response(
            {
                "data": service.get_trainings_type_ratio(
                    serializer.data["period"]
                ),
            }
        )


class GetAvgCaloriesPerDayInfo(GenericAPIView):
    serializer_class = PeriodSerializer

    def get(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        service = UserStatisticService(request.user)
        return Response(
            {
                "data": service.get_avg_calories(
                    serializer.data["period"]
                )
            }
        )


class GetAvgProteinPerDayView(GenericAPIView):
    serializer_class = PeriodSerializer

    def get(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        service = UserStatisticService(request.user)
        return Response(
            {
                "data": service.get_avg_protein(
                    serializer.data["period"]
                )
            }
        )


class GetAvgCarbohydratesPerDayView(GenericAPIView):
    serializer_class = PeriodSerializer

    def get(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        service = UserStatisticService(request.user)
        return Response(
            {
                "data": service.get_avg_carbohydrates(
                    serializer.data["period"]
                )
            }
        )


class GetAvgFatsPerDayView(GenericAPIView):
    serializer_class = PeriodSerializer

    def get(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        service = UserStatisticService(request.user)
        return Response(
            {
                "data": service.get_avg_fats(
                    serializer.data["period"]
                )
            }
        )


class GetTotalKmTraining(GenericAPIView):
    training_type: type[Training]
    serializer_class = PeriodSerializer

    def get(self, request) -> Response:
        serializer = self.get_serializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        service = UserStatisticService(request.user)
        response = Response(
            {
                "data": service.get_total_km(
                    serializer.data["period"],
                    self.training_type,
                ),
                "code": status.HTTP_200_OK,
            },
        )
        return response


class GetTotalKMbyCycling(GetTotalKmTraining):
    training_type = Cycling


class GetTotalKMbyJogging(GetTotalKmTraining):
    training_type = Jogging


class GetTotalKMbyWalking(GetTotalKmTraining):
    training_type = Walking


class GetTotalKMbySwimming(GetTotalKmTraining):
    training_type = Swimming


class GetPFCratio(GenericAPIView):
    serializer_class = PeriodSerializer

    def get(self, request) -> Response:
        serializer = self.get_serializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        service = UserStatisticService(request.user)

        return Response(
            {
                "data": service.get_pfc_ratio(
                    serializer.data["period"],
                ),
                "code": status.HTTP_200_OK,
            },
        )