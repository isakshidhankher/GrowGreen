from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[

   path('forum', views.forum, name='forum'),
   path('forum-detail/<int:post_id>', views.blog_post, name='forum-detail'),
   
   path('write-post', views.new_post, name='write-post'),
   path('forum-search', views.forum_search, name='forum-search'),
   ]  