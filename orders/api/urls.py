from django.urls import path
from orders.views.address import AddressList
from orders.views.order import OrderList, create_order
from orders.views.payment import get_payment_link , PaymentMethodsList, payment_status



urlpatterns = [
    path("goves",AddressList.as_view()),
    path("orders",OrderList.as_view()),
    path("create-order",create_order),
    path("payment-link",get_payment_link),
    path("payment-methods",PaymentMethodsList.as_view()),
    path("payment-status",payment_status),
]