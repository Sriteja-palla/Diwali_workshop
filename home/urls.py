from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('add-cracker/', views.add_crakers, name='add_cracker'),
    path('add-sweet/', views.add_sweets, name='add_sweet'),
    path('add-gift/', views.add_gifts, name='add_gift'),
    path('', views.register, name='register'),
    path('add-to-cart/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/increase/<int:cart_id>/', views.increase_qty, name='increase_qty'),
    path('cart/decrease/<int:cart_id>/', views.decrease_qty, name='decrease_qty'),
    path('cart/remove/<int:cart_id>/', views.remove_item, name='remove_item'),
    path('logout/', views.user_logout, name='logout'),
    path('place-order/',views.place_order,name='place_order'),
]