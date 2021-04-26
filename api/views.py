from django.db.models.aggregates import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import (
    filters,
    mixins,
    viewsets
)

from .filters import TitleFilter
from .models import (
    Categories,
    Genres,
    Review,
    Title
)
from .permissions import (
    IsAdminOrReadOnly,
    IsOwnerAdminModerator
)
from .serializers import (
    CategoriesSerializer,
    CommentSerializer, GenresSerializer,
    ReviewSerializer, TitleReadSerializer,
    TitleWriteSerializer
)


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if (self.action == 'list') or (self.action == 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class CategoriesViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filterset_fields = ('name',)
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', ]
    permission_classes = [IsAdminOrReadOnly]


class GenresViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filterset_fields = ('name',)
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', ]
    permission_classes = [IsAdminOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerAdminModerator]

    def get_queryset(self):

        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerAdminModerator]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'],
                                   title=self.kwargs['title_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'],
                                   title=self.kwargs['title_id'])
        serializer.save(author=self.request.user, review=review)
