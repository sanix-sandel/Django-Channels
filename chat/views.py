from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json
from .models import*


from rest_framework import generics
from .serializers import ConversationSerializer


class ConversationListView(generics.ListAPIView):

    queryset=Conversation.objects.all()
    serializer_class=ConversationSerializer


@login_required
def chat_room(request, id):
   # print(other_id)
    user2=get_object_or_404(get_user_model(), id=id)
    
    conversation=Conversation.objects.filter(users=request.user).filter(users=user2).first()
    print(conversation)
    print(request.user.id)
    if conversation==None:
        #users=[request.user, user2]
        conversation=Conversation.objects.create(code=str(request.user.id)+str(user2.id))
        conversation.users.set([request.user, user2])
        conversation.save()
        print(conversation)
      
    return render(request, 
                'chat/room.html', 
                {   
                    'room_name':conversation.code,
                    'user':request.user,
                    'user2':user2
                })  