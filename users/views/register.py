from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from users.api.serializers import RegisterSerializer




User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer



    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        if User.objects.filter(email=email).exists():
            return Response({"detail": "هذا البريد الالكترونى مسجل من قبل"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({"detail": "رقم الهاتق هذا مسجل من قبل"}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
