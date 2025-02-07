from django.urls import path
from products.views.home import HomeList
from products.views.products import ProductsList


urlpatterns = [
    path("products",ProductsList.as_view()),
    path("home-products",HomeList.as_view())
]