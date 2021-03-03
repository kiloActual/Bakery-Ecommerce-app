import django_filters
from .models import *

class Orderfilter(django_filters.FilterSet):
    class Meta:
        model = OrderItem
        fields = '__all__'