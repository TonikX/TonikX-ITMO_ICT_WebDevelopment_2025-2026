from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import FileViewSet, FolderViewSet, PublicSharedFileView


router = DefaultRouter()
router.register(r"files", FileViewSet, basename="file")
router.register(r"folders", FolderViewSet, basename="folder")

urlpatterns = [
    path("", include(router.urls)),
    path("p/<str:token>/", PublicSharedFileView.as_view(), name="public-file"),
]