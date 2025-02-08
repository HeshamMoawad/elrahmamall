from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from ..models import Category , Brand ,Product
from ..api.serializers import CategorySerializer , BrandSerializer , ProductSerializer , HomeSerializer
from rest_framework.generics import ListAPIView


class HomeList(ListAPIView):
    queryset = Category.objects.filter(hide=False)
    serializer_class = HomeSerializer
