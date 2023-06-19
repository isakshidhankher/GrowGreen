from django.urls import path
from . import views

from . import views

# chat stuff
urlpatterns = [
    path('test0', views.test0, name='test0'),
    path('test1/<int:id>', views.test1),
    path('test2/', views.test2),
    # path('<str:room_name>/', views.room, name='room'),
    path('test/<str:room_name>/', views.test, name='test'),

    path('create_chat/<int:id>', views.create_chat, name='create-chat'),


    path('chat_new', views.chat_new),
]