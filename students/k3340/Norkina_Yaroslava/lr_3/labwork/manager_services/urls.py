from django.urls import path
from . import views

urlpatterns = [
    path('api/services/', views.ServiceListAPIView.as_view(), name='service-list'),
    path('api/services/<int:pk>/', views.ServiceDetailAPIView.as_view(), name='service-detail'),
    path('api/services/categories/', views.ServiceCategoriesAPIView.as_view(), name='service-categories'),

    path('api/admin/services/', views.AdminServiceListAPIView.as_view(), name='admin-service-list'),
    path('api/admin/services/<int:pk>/', views.AdminServiceDetailAPIView.as_view(), name='admin-service-detail'),
    path('api/admin/services/<int:pk>/deactivate/', views.AdminServiceDeactivateAPIView.as_view(),
         name='admin-service-deactivate'),

    path('api/admin/files/upload/', views.AdminFileUploadAPIView.as_view(), name='admin-file-upload'),
    path('api/admin/files/<int:pk>/', views.AdminFileDetailAPIView.as_view(), name='admin-file-detail'),
    path('api/services/<int:service_id>/files/', views.ServiceFilesAPIView.as_view(), name='service-files'),

    path('api/orders/', views.OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('api/orders/<int:pk>/', views.OrderDetailAPIView.as_view(), name='order-detail'),
    path('api/orders/<int:pk>/cancel/', views.OrderCancelAPIView.as_view(), name='order-cancel'),

    path('api/admin/orders/', views.AdminOrderListAPIView.as_view(), name='admin-order-list'),
    path('api/admin/orders/<int:pk>/', views.AdminOrderDetailAPIView.as_view(), name='admin-order-detail'),
    path('api/admin/orders/<int:pk>/status/', views.AdminOrderStatusUpdateAPIView.as_view(), name='admin-order-status'),
    path('api/admin/orders/<int:pk>/history/', views.AdminOrderHistoryAPIView.as_view(), name='admin-order-history'),

    path('api/orders/<int:order_id>/comments/', views.OrderCommentsAPIView.as_view(), name='order-comments'),

    path('api/admin/comments/', views.AdminCommentListAPIView.as_view(), name='admin-comment-list'),
    path('api/admin/comments/<int:pk>/', views.AdminCommentDetailAPIView.as_view(), name='admin-comment-detail'),
    path('api/admin/comments/<int:pk>/visibility/', views.AdminCommentVisibilityAPIView.as_view(),
         name='admin-comment-visibility'),

    path('api/services/<int:service_id>/reviews/', views.ServiceReviewsAPIView.as_view(), name='service-reviews'),
    path('api/reviews/', views.UserReviewCreateAPIView.as_view(), name='review-create'),
    path('api/reviews/<int:pk>/', views.ReviewDetailAPIView.as_view(), name='review-detail'),

    path('api/admin/reviews/', views.AdminReviewListAPIView.as_view(), name='admin-review-list'),
    path('api/admin/reviews/pending/', views.AdminPendingReviewsAPIView.as_view(), name='admin-pending-reviews'),
    path('api/admin/reviews/<int:pk>/', views.AdminReviewDetailAPIView.as_view(), name='admin-review-detail'),
    path('api/admin/reviews/<int:pk>/publish/', views.AdminReviewPublishAPIView.as_view(), name='admin-review-publish'),

    path('api/admin/users/', views.AdminUserListAPIView.as_view(), name='admin-user-list'),
    path('api/admin/users/<int:pk>/', views.AdminUserDetailAPIView.as_view(), name='admin-user-detail'),
    path('api/admin/users/<int:pk>/role/', views.AdminUserRoleUpdateAPIView.as_view(), name='admin-user-role'),
]
