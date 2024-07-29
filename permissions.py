from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedAndOwnerPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (
            hasattr(obj, "user")
            and request.user == obj.user
        )


class IsAuthenticatedAndPowerTrainingExerciseOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (
            hasattr(obj, "power_training")
            and obj.power_training.user == request.user
        )


class IsAuthenticatedAndApproachOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (
            hasattr(obj, "training")
            and obj.training.power_training.user == request.user
        )
