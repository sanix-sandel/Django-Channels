from django.urls import path
from . import views

urlpatterns=[
    path('api/users', views.UserListView.as_view()),
]