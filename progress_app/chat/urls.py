from django.urls import path
from . import views

urlpatterns = [
    path("create_group/", views.create_group, name="create_group"),
    path(
        "add_member/<int:group_id>/",
        views.add_member_to_group,
        name="add_member_to_group",
    ),
    path("list_groups/", views.list_groups, name="list_groups"),
    path(
        "send_message/<int:group_id>/",
        views.send_message_to_group,
        name="send_message_to_group",
    ),
]
