from django.urls import path
from . import views

urlpatterns = [
    path('',views.store,name='store'),
    path('shop/',views.shop,name='shop'),
    path('customize-cake/',views.customCake,name='customCake'),
    path('products/<str:pk1>/<str:pk2>/',views.singleProduct,name='products'),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name='checkout'),
    path('register/',views.registerUser,name="register"),
    path('login/',views.loginUser,name="login"),
    path('logout/',views.logoutUser,name='logout'),
    path('update_item/',views.updateItem,name="update_item"),
    path('update_custom_item/',views.updateCustomItem,name='update_custom_item'),
    path('proccess_order/',views.proccessOrder,name="proccess_order"),
    path('update_item_single_page/',views.updateItemForSinglePage,name='update_item_single_page'),
    #seller
    path('dashboard/',views.dashboard,name='dashboard'),
    path('product/',views.product,name='product'),
    path('customer/<str:pk>/',views.userInfo,name='customer'),
    path('edit_status/<str:pk>/',views.editstatus,name='editstatus'),
    path('edit_custom_status/<str:pk>/',views.editCustomStatus,name='edit_custom_status'),
    path('delete/<str:pk>/',views.deleteProduct,name='deleteProduct'),
]
