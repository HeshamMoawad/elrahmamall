from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from users.api.serializers import LoginSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email_or_phone = serializer.validated_data['email_or_phone']
        password = serializer.validated_data['password']

        user = authenticate(request, username=email_or_phone, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = Response({
                **UserSerializer(user).data,
                # 'refresh': str(refresh),
                'access': str(refresh.access_token),
                "expire" :datetime.utcfromtimestamp(refresh.access_token['exp']).isoformat()
            })
            response.set_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"],str(refresh.access_token))
            return response
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)