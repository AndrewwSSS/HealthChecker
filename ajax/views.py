from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from ajax.forms import UserUpdateForm
from main.models import User


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
        }
    )


@login_required
def update_user(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse(
            {
                "status": "Method not allowed"
            },
            status=405
        )

    form = UserUpdateForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        return JsonResponse({
            "status": "success",
        }, status=200)

    return JsonResponse(
        {
            "status": "error",
            "errors": form.errors,
        }
    )

