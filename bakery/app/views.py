from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import *
from .forms import *
from .filters import *
from .decorators import *
import json,sys
from collections import Counter 
import datetime
from django.contrib.auth.decorators import login_required

@seller_or_customer
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
    products = Product.objects.all().order_by('-id')
    context = {'products': products,'order': order}
    return render(request,'app/store.html',context)

@seller_or_customer
def shop(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
    products = Product.objects.all().order_by('-id')
    context = {'products': products,'order': order}
    return render(request,'app/shop.html',context)    

@seller_or_customer
@login_required(login_url='login')
def customCake(request):
    form = Createcustomitem()
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    if request.method == 'POST':
        form = Createcustomitem(request.POST)
        if form.is_valid():
           customitem = form.save(commit=False)
           customitem.order = order
           customitem.status = 'Pending'
           customitem.save()
           form.save_m2m()
    context = {'form':form,'order':order}
    return render(request,'app/custom_cake.html',context)

@seller_or_customer
def singleProduct(request,pk1,pk2):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
    product = Product.objects.get(id=pk1,name=pk2)
    context={'product':product,'order': order}
    return render(request,'app/singleProduct.html',context)

@seller_or_customer
def updateItemForSinglePage(request):
    data = json.loads(request.body)
    productId = data['ProductId']
    updateQunt = data['updateQunt']
    print('productId:',productId)
    print('updateQunt:',updateQunt)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)
    
    orderItem.quantity = updateQunt
    orderItem.save()
    return JsonResponse("Update Item.",safe=False)

@login_required(login_url='login')
@seller_or_customer
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        items2 = order.customitem_set.all()
        print(items2)
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
    context = {'items':items,'order':order,'items2':items2}        
    return render(request,'app/cart.html',context)    

@login_required(login_url='login')
@seller_or_customer
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        items2 = order.customitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
    context = {'items':items,'order':order,'items2':items2}  
    return render(request,'app/checkout.html',context)

@unauthenticated_user
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('store')
        else:
            messages.info(request,"Username or Password is incorrect.")    
    context = {}
    return render(request,'app/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def registerUser(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
            user = user,
            email=email,
            )
            messages.success(request,'Account is created successfully for ' + username + '.')
            return redirect('login')


    context = {'form':form}
    return render(request,'app/register.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('action:',action)
    print('productId:',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

    orderItem.status = 'Pending'
        
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()


    if orderItem.quantity <= 0:
        orderItem.delete()        
    return JsonResponse("Item added..",safe=False)

def updateCustomItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('action:',action)
    print('productId:',productId)

    customer = request.user.customer

    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    customitem, created = CustomItem.objects.get_or_create(id=productId,order=order)
    
    if action == 'add':
        customitem.quantity = (customitem.quantity + 1)
    elif action == 'remove':
        customitem.quantity = (customitem.quantity - 1)
    customitem.save()

    if customitem.quantity <= 0:
        customitem.delete()        
    return JsonResponse("Item added..",safe=False)

def proccessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print(data)
    if request.user.is_authenticated:
        customer = request.user.customer
        user = request.user
        
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        order.transaction_id = transaction_id
        customer, created = Customer.objects.get_or_create(user=user)
        customer.name=name=data['userFormData']['name']
        customer.phone=data['userFormData']['phone']
        customer.save()
        total = float(data['userFormData']['total'])
        if order.get_cart_total == total:
            order.complete = True
        order.save()
        

        Shippingaddress.objects.create(
            customer=customer,
            order=order,
            address=data['shippingInfo']['address'],      
            city=data['shippingInfo']['city'],
            state=data['shippingInfo']['state'],
            zipcode=data['shippingInfo']['zipcode'],
        )    

    return JsonResponse("order Complete",safe=False)

#seller functions
@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def dashboard(request):
    order = []
    customorder = []
    status = []
    sellerItem = request.user.seller.product_set.all()
    customitem = request.user.seller.customitem_set.all()
    for new in customitem:
        if new.order.complete == True: 
                customorder.append(new)
    for product in sellerItem:
        orders = product.orderitem_set.all()
        for i in orders: 
            if i.order.complete == True: 
                order.append(i)
                status.append(i.status) 
    statusCount = Counter(status)                            
    context = {'orders':order,'pending':statusCount['Pending'],'ourfordelivery':statusCount['Out for delivery'],'delivered':statusCount['Delivered'],'customitem':customorder}
    return render(request,'seller/dashboard.html',context)    

@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def product(request):
    form = CreateProduct()
    products = request.user.seller.product_set.all().order_by('-id')

    if request.method == 'POST':
        form = CreateProduct(request.POST,request.FILES)
        if form.is_valid():
           product = form.save(commit=False)
           product.seller = request.user.seller
           product.save()
           form.save_m2m()
           
    context = {'products':products,'form':form}
    return render(request,'seller/product.html',context)  

@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def userInfo(request,pk):
    temp = []
    sellerItem = request.user.seller.product_set.all()
    customitem = request.user.seller.customitem_set.all()
    for j in customitem:
        temp.append(j.order.id)
    for product in sellerItem:
        orders = product.orderitem_set.all()
        for i in orders:
            temp.append(i.order.id)
    if int(pk) in temp:
        shipping = Shippingaddress.objects.get(order=pk)
        context = {'shipping':shipping}
    else:
        return redirect('dashboard')
        context={}    
    return render(request,'seller/userinfo.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def editstatus(request,pk):
    temp = []
    sellerItem = request.user.seller.product_set.all()
    for product in sellerItem:
        orders = product.orderitem_set.all()
        for i in orders:
            if i.order.complete == True: 
                temp.append(i.id) 
    if int(pk) in temp:      
        orderitem = OrderItem.objects.get(id=pk)
        form = Createorderitem(instance=orderitem)  
        if request.method == 'POST':
            form = Createorderitem(request.POST,instance=orderitem)
            if form.is_valid():
                form.save()
                return redirect('dashboard') 
        context = {'form':form}
    else:
        return HttpResponse('You Are On Unauthorized Page.')   
    return render(request,'seller/crud_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def editCustomStatus(request,pk):
    temp = []
    customitem = request.user.seller.customitem_set.all()
    for product in customitem:  
        if product.order.complete == True: 
            temp.append(product.id) 
    if int(pk) in temp:      
        customitem = CustomItem.objects.get(id=pk)
        form = Createcustomitem2(instance=customitem)  
        if request.method == 'POST':
            form = Createcustomitem2(request.POST,instance=customitem)
            if form.is_valid():
                form.save()
                return redirect('dashboard') 
        context = {'form':form}
    else:
        return HttpResponse('You Are On Unauthorized Page.')   
    return render(request,'seller/crud_form.html',context)    

@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def deleteProduct(request,pk):
    productId=[]
    product = Product.objects.get(id=pk)
    sellerItem = request.user.seller.product_set.all()
    for i in sellerItem:
        productId.append(i.id)    
    if int(pk) in productId:
        if request.method == 'POST':
            product.delete()
            return redirect('product')
    else:
        return redirect('product')        
    context = {'product':product}
    return render(request,'seller/delete.html',context)