
from django.urls import path
from .import views as v


urlpatterns = [
    path('',v.Index.as_view(),name='homepage'),
    path('home',v.home),
    path('signup',v.signup),
    path('login',v.login,name='login'),
    path('logout',v.logout,name='logout'),
    path('cart',v.Cart.as_view(),name='cart'),
    path('checkout',v.Checkout.as_view(),name='checkout'),
    path('orders',v.OrderView.as_view(),name='orders'),
    
]
