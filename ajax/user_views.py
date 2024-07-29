from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.views import View

from ajax.forms import UserUpdateForm
from ajax.views import SUCCESS_RESPONSE


class UpdatePasswordView(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return JsonResponse(
                {
                    "status": "success",
                },
                status=200,
            )

        return JsonResponse(
            {
                "status": "error",
                "errors": form.errors,
            },
            status=422,
        )


class UpdateUser(LoginRequiredMixin, View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return SUCCESS_RESPONSE

        return JsonResponse(
            {
                "status": "error",
                "errors": form.errors,
            },
            status=422,
        )