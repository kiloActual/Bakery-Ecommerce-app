from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class CreateProduct(ModelForm):
    class Meta:
        model = Product        
        fields ='__all__'
        exclude = ['seller']

class Createorderitem(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['status']

class Createcustomitem(ModelForm):
    class Meta:
        model = CustomItem
        fields = '__all__'
        exclude = ['order','status']

class Createcustomitem2(ModelForm):
    class Meta:
        model = CustomItem
        fields = ['status']