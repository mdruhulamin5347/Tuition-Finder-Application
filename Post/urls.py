from django.urls import path
from .views import post_view, PostListView, PostDetailView, PostUpdateView, post_delete, search, filter, like_post, comment, add_photo, notification, delete_comment, apply, post_views

urlpatterns = [
    path('post-create', post_view, name='post_create'),  # Renamed to `post_create` for clarity
    path('', PostListView.as_view(), name='post_list'),
    path('post-details/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post-edit/<int:pk>/', PostUpdateView.as_view(), name='post_edit'),
    path('post-delete/<int:id>/', post_delete, name='post_delete'),
    path('post-likepost/<int:id>/', like_post, name='like_post'),
    path('tuition-apply/<int:id>/', apply, name='post_apply'),
    path('post-deletecomment/<int:id>/', delete_comment, name='delete_comment'),
    path('post-notification/', notification, name='notification'),
    path('post-picadd/<int:id>/', add_photo, name='add_photo'),
    path('search/', search, name='search'),
    path('filter/', filter, name='filter'),
    path('post-comment/', comment, name='comment'),
    path('post-postviews/', post_views, name='post_views'),
]