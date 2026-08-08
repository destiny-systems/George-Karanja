from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio_home, name='portfolio_home'),
    path('property/<slug:slug>/', views.property_detail, name='property_detail'),
    path('checkout/<int:floor_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
]
