from django.urls import path
from django.urls.resolvers import URLPattern
from client.views import ProductionList, OrderCreate, OrderCustomizations


urlpatterns = [
    path('products/', ProductionList.as_view()),
    path('order/', OrderCreate.as_view()),
    path('order/customization/<int:pk>/', OrderCustomizations.as_view()),
]