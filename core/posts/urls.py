from django.urls import path
from .views import PostListCreateView, PostDeleteView, PostLikeToggleView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('<int:pk>/like/', PostLikeToggleView.as_view(), name='post-like-toggle'),
]
