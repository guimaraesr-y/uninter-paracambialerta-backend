from django.utils.translation import gettext as _

from rest_framework import serializers

from src.users.models import BasicUser


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        user = BasicUser.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
