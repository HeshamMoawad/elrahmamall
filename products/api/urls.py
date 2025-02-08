from django.urls import path
from products.views.home import HomeList
from products.views.products import ProductsList
from products.views.category import CategoryList
from products.views.brands import BrandList


urlpatterns = [
    path("brands",BrandList.as_view()),
    path("products",ProductsList.as_view()),
    path("categories",CategoryList.as_view()),
    path("home-products",HomeList.as_view())
]