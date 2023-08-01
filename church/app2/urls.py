from django.urls import path

from church.users.views import user_detail_view, user_redirect_view, user_update_view

from . import views
from django.views.generic import TemplateView
app_name = "app2"

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path("add_member/", views.add_member_to_group, name="add_member_to_group"),
    path("sermons/", views.sermon_list, name="sermon_list"),
    path("send-sms/", views.send_sms, name="send_sms"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("members/", views.members_view, name="members"),
    path("member/<int:member_id>/", views.member_detail, name="member_detail"),
    path("group/create/", views.create_group, name="create_group"),
    path("group/<int:group_id>/", views.group_detail, name="group_detail"),
]