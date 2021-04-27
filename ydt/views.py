from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import firebase_admin
from firebase_admin import auth, db, credentials
from django.core import serializers

from .serializers import UserSerializer, UserSerializerWithToken, TodoSerializer, TokenSerializer
from .models import Todo
cred = credentials.Certificate("ydt/serviceAccountKey.json")
if not firebase_admin._apps:
    # app = firebase_admin.initialize_app()
    app = firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://yrkesdorren-bfdfc-default-rtdb.europe-west1.firebasedatabase.app/'
    })    

@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """   
    custom_token = auth.create_custom_token(str(request.user)) 
    ts = TokenSerializer({
        'firebase_token': custom_token,
        'username': request.user
        })

    return Response(ts.data, status=status.HTTP_200_OK)

def update_firebase(queryset):
    ref = db.reference('/')
    ref.delete()
    objects_to_save = {}
    for instance in queryset:
        objects_to_save[instance.id] = {
            'id': instance.id,
            'title': instance.title,
            'description': instance.description,
            'responsible': instance.responsible,
            'author': instance.author,
            'isCompleted': instance.isCompleted,
            'created_at': str(instance.created_at),
            'update_at': str(instance.update_at)
        }
    ref.set(objects_to_save)
    
class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)        
        update_firebase(Todo.objects.all())

    def perform_update(self, serializer):
        serializer.save()        
        update_firebase(Todo.objects.all())

    def perform_destroy(self, serializer):
        serializer.delete() 
        update_firebase(Todo.objects.all())
