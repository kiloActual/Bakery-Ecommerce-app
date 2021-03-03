from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(default='Yourname',max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    data_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name

class Seller(models.Model):
    user = models.OneToOneField(User,null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(default='Sellername',max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    data_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    RATE = ((1,1),(2,2),(3,3),(4,4),(5,5))
    seller = models.ForeignKey(Seller,null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    price = models.DecimalField(max_digits=7,decimal_places=2,null=True)
    rating = models.IntegerField(null=True,choices=RATE)
    image = models.ImageField(null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''  
        return url      

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True)
    data_orderd = models.DateTimeField(auto_now_add=True)
    complete =  models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.customer.user.username

    @property    
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        customitems = self.customitem_set.all() 
        a = sum([i.get_total for i in orderitems])
        b = sum([i.get_total for i in customitems])
        total = sum([a,b])
        return total

    @property    
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        customitems = self.customitem_set.all() 
        a = sum([i.quantity for i in orderitems])
        b = sum([i.quantity for i in customitems])
        total = sum([a,b])
        return total
class Size(models.Model):
    name = models.CharField(max_length=200,null=True) 
    price = models.DecimalField(max_digits=7,decimal_places=2,null=True)
    def __str__(self):
        return self.name      

class Flavor(models.Model):
    name = models.CharField(max_length=200,null=True)     
    price = models.DecimalField(max_digits=7,decimal_places=2,null=True)
    def __str__(self):
        return self.name  

class Shape(models.Model):
    name = models.CharField(max_length=200,null=True)  
    def __str__(self):
        return self.name   
        

class CustomItem(models.Model):
    STATUS = (('Pending','Pending'),
                ('Out for delivery','Out for delivery'),
                ('Delivered','Delivered'))
    seller = models.ForeignKey(Seller,null=True,blank=True, on_delete=models.CASCADE)            
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True) 
    size = models.ForeignKey(Size,on_delete=models.SET_NULL,blank=True,null=True)
    flavor = models.ForeignKey(Flavor,on_delete=models.SET_NULL,blank=True,null=True)
    shape = models.ForeignKey(Shape,on_delete=models.SET_NULL,blank=True,null=True)
    name_on_cake =  models.CharField(max_length=200,null=True)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)],null=True,blank=True)
    data_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=200,null=True,choices=STATUS)
    @property
    def get_product_total(self):
        total = (self.flavor.price + self.size.price)
        return total
    @property
    def get_total(self):
        total = (self.flavor.price + self.size.price) * self.quantity
        return total

class OrderItem(models.Model):
    STATUS = (('Pending','Pending'),
                ('Out for delivery','Out for delivery'),
                ('Delivered','Delivered'))
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True) 
    quantity = models.IntegerField(default=0,null=True,blank=True)
    data_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200,null=True,choices=STATUS)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class Shippingaddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)       
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

