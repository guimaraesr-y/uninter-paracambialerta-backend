from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class UserLoginView(ObtainAuthToken):
    """
    API endpoint for user login.
    Returns an auth token.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        if (
            not isinstance(validated_data, dict)
            or 'user' not in validated_data
        ):
            return Response(
                {'error': 'Invalid login credentials.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


user_login_view = UserLoginView.as_view()
