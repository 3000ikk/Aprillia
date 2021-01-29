from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.http import require_http_methods

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import permissions as p, viewsets, status, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from rest_framework.response import Response

from django.db.models import Q

from .serializers import *
from .filters import *
from .models import *
from .utils import IsAuthor


class MyPagination(PageNumberPagination):
    page_size = 3


class CategoriesList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = MyPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = ProductFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductSerializer
        elif self.action == 'list':
            return ProductListSerializer
        return CreateUpdateProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'search']:
            permissions = []
        else:
            permissions = [p.IsAdminUser]
        return [permission() for permission in permissions]

    @action(methods=['GET'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        if q is not None:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        serializer = ProductSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateComment(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (p.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    GenericViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthor]
    serializer_class = CommentSerializer


