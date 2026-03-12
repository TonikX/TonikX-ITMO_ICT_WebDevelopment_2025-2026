from rest_framework.routers import DefaultRouter
from .views import HallViewSet, BookViewSet, ReaderViewSet, BookIssueViewSet, BookInHallViewSet

router = DefaultRouter()

router.register('halls', HallViewSet)
router.register('books', BookViewSet)
router.register('books-in-halls', BookInHallViewSet)
router.register('readers', ReaderViewSet)
router.register('issues', BookIssueViewSet)

urlpatterns = router.urls