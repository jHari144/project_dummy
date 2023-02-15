from django.urls import path

from . import views

app_name='post_db'
urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        path('<int:pk>/', views.DetailView.as_view(), name='detail'),
        path('create_post/', views.create_post, name='create_post'),
        path('<int:post_id>/edit_post/', views.edit_post, name='edit_post'),
        path('<int:pk>/upvote', views.upvote, name='upvote'),
        path('<int:pk>/downvote', views.downvote, name='downvote'),
]

