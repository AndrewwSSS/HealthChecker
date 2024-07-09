from django.urls import path

from ajax.views import change_password, update_user, add_power_exercise

urlpatterns = [
    path("user_update", update_user, name="user_update"),
    path("change_password", change_password, name="change_password"),
    path("add_power_training_exercise", add_power_exercise, name="add_power_training_exercise"),
]

app_name = 'ajax'
