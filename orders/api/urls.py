from django.urls import path
from orders.views.address import AddressList



urlpatterns = [
    path("goves",AddressList.as_view()),
]