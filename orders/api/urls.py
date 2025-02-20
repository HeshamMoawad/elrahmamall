from django.urls import path
from orders.views.address import AddressList
from orders.views.order import OrderList, create_order



urlpatterns = [
    path("goves",AddressList.as_view()),
    path("orders",OrderList.as_view()),
    path("create-order",create_order),
]