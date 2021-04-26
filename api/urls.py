from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesViewSet,
    CommentViewSet,
    GenresViewSet,
    ReviewViewSet,
    TitleViewSet
)

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet, basename='Titles')
v1_router.register('genres', GenresViewSet, basename='Genres')
v1_router.register('categories', CategoriesViewSet, basename='Categories')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
