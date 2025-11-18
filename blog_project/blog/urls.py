from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('blog/', PostListView.as_view(), name='post_list'),
    path('blog/write/', PostCreateView.as_view(), name='write_post'),
    path('blog/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('blog/search/<str:tag>/', PostSearchView.as_view(), name='search_posts'),
    path('blog/edit/<int:pk>/', PostUpdateView.as_view(), name='edit_post'),
    path('blog/delete/<int:pk>/', PostDeleteView.as_view(), name='delete_post'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)