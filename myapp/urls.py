from django.urls import path
from . import views 
urlpatterns = [
    path('getPolicy',views.getPolicy),
    path('getProduct',views.getProduct),
    path('listProduct',views.listProduct),
    path('removeProduct',views.removeProduct),
]