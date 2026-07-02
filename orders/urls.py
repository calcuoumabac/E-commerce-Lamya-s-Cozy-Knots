from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/<int:variant_id>/', views.cart_add, name='cart_add'),
    path('remove/<str:key>/', views.cart_remove, name='cart_remove'),
    path('update/<str:key>/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('confirmed/<int:order_id>/', views.order_confirmed, name='confirmed'),
]