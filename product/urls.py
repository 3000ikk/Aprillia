from django.urls import path, include
from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register('', ProductViewSet)
# router.register('', CreateComment)


urlpatterns = [
    path('categories/', CategoriesList.as_view()),
    path('', include(router.urls)),
    path('comments/create/', CreateComment.as_view()),
    path('comments/<int:pk>/', CommentViewSet.as_view({
        "get": "retrieve",
        "path": "partial_update",
        "put": "update",
        "delete": "destroy"}))
]