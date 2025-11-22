from django.contrib import admin
from .models import Client, Employee, ServiceCategory, Service, Order, PaymentOrder

admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(ServiceCategory)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(PaymentOrder)
