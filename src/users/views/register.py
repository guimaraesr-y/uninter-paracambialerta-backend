from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from src.users.models import BasicUser
from src.users.serializers import UserRegistrationSerializer


class UserRegistrationView(APIView):
    """
    API endpoint for user registration.
    """
    permission_classes = []
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if not isinstance(user, BasicUser):
                return Response(
                    {"error": "User registration failed"},
                    status.HTTP_400_BAD_REQUEST
                )

            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


user_register_view = UserRegistrationView.as_view()
