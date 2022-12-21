from django.urls import path
from .views import PostList, PostDetail, PostListFiltered, PostCreateView, PostListWithFilters, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('search/', PostListFiltered.as_view(), name='search'),
    path('search2/', PostListWithFilters.as_view()),
]
