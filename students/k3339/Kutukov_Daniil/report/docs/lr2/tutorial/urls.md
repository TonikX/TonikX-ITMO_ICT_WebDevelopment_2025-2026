# URL маршруты Tutorial

## Основные маршруты

```python
urlpatterns = [
    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/create/', CarCreateView.as_view(), name='car_create'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
    
    path('owners/', OwnerListView.as_view(), name='owner_list'),
    # аналогично для owners
    
    path('licenses/', DriverLicenseListView.as_view(), name='license_list'),
    # аналогично для licenses
]
```