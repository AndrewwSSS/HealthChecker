from django.contrib.auth import update_session_auth_hash
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from ajax.serializers import ChangePasswordSerializer
from ajax.serializers import UserUpdateSerializer


class UpdatePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(request.data['old_password']):
            return Response(
                {"old_password": ["Wrong password."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(request.data.get("new_password1"))
        user.save()
        update_session_auth_hash(request, user)
        return Response(
            {
                "status": "success",
                "code": status.HTTP_200_OK
            },
        )


class UserUpdateView(UpdateAPIView):
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user
