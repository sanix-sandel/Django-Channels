from django.urls import path
from . import views


app_name='chat'

urlpatterns = [
    path('<int:id>', views.chat_room, name='chat_room'),   
    path('api/convs', views.ConversationListView.as_view()), 
]