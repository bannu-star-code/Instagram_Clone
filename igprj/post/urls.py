from django.urls import path
from post import views

urlpatterns=[
    path('',views.index,name='index'),
    path('newpost/',views.NewPost, name='newpost'),
    path('<uuid:post_id>',views.PostDetail,name='post-details'),
    path('tag/<slug:tag_slug>',views.Tags, name='tags'),
    path('<uuid:post_id>/like',views.like, name='like'),
    path('like',views.like_ajax, name='like_ajax'),
    path('favourite', views.favourite_ajax, name='favourite_ajax'),
    path('<uuid:post_id>/favourite', views.favourite, name='favourite'),
    path('<uuid:post_id>/delete', views.delete, name='delete'),
]