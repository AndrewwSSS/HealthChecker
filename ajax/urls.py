from django.urls import path

from ajax.views import (change_password,
                        update_user,
                        add_power_exercise,
                        delete_exercise,
                        delete_approach,
                        add_approach, delete_training)

urlpatterns = [
    path("user_update", update_user, name="user_update"),
    path("change_password", change_password, name="change_password"),
    path("add_power_training_exercise", add_power_exercise, name="add_power_training_exercise"),
    path("delete_exercise", delete_exercise, name="delete_exercise"),
    path("delete_approach", delete_approach, name="delete_approach"),
    path("add_approach", add_approach, name="add_approach"),
    path("trainings/delete_training", delete_training, name="delete_training"),
]

app_name = 'ajax'
