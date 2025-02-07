from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from ..models import Category , Brand ,Product
from ..api.serializers import CategorySerializer , BrandSerializer , ProductSerializer , HomeSerializer
from rest_framework.generics import ListAPIView

# @api_view(['GET'])
# def home_products(request):
#     categories = 
#     return Response(HomeSerializer(categories,many=True).data)


class HomeList(ListAPIView):
    queryset = Category.objects.filter(hide=False)
    serializer_class = HomeSerializer
