from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Shippingaddress)
admin.site.register(Seller)
admin.site.register(Size)
admin.site.register(Flavor)
admin.site.register(Shape)
admin.site.register(CustomItem)