from django.urls import path

from ajax.views import change_password, update_user

urlpatterns = [
    path("user_update", update_user, name="user_update"),
    path("change_password", change_password, name="change_password"),
]

app_name = 'ajax'
