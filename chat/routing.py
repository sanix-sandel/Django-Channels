from django.urls import path

from . import consumers

websocket_urlpatterns=[
    path('ws/chat/<str:roomName>/<str:user2_id>/', consumers.ChatConsumer),
]