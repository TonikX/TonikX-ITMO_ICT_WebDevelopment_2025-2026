from django.contrib import admin

from .models import Batch, BatchItem, Broker, BrokerCompany, Manufacturer, Product

admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(BrokerCompany)
admin.site.register(Broker)
admin.site.register(Batch)
admin.site.register(BatchItem)

