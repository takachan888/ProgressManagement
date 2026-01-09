from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("me/", views.my_tasks, name="my_tasks"),
    path("leader/", views.leader_dashboard, name="leader_dashboard"),
    path("task/<int:task_id>/update/", views.update_task, name="update_task"),
    path("after-login/", views.after_login, name="after_login"),
    path("leader/task/new/", views.leader_task_create, name="leader_task_create"),
    path("leader/task/<int:task_id>/edit/", views.leader_task_edit, name="leader_task_edit"),
    path("leader/task/<int:task_id>/delete/", views.leader_task_delete, name="leader_task_delete"),
    path("leader/users/", views.leader_user_list, name="leader_user_list"),
    path("leader/users/new/", views.leader_user_create, name="leader_user_create"),
    path("leader/users/<int:user_id>/edit/", views.leader_user_edit, name="leader_user_edit"),
    path("leader/users/<int:user_id>/delete/", views.leader_user_delete, name="leader_user_delete"),



]
