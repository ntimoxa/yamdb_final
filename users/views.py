from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin, IsOwner
from .serializers import ConfirmSerializer, EmailSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]
    lookup_field = "username"
    lookup_value_regex = "[^/]+"

    @action(detail=False, methods=['get', 'patch'], permission_classes=[
        IsAuthenticated, IsOwner, ])
    def me(self, request):
        self.kwargs['username'] = request.user.username

        if request.method == 'GET':
            return self.retrieve(request)
        elif request.method == 'PATCH':
            return self.partial_update(request)

        else:
            raise Exception('Not implemented')


def send_msg(email, confirmation_code):
    subject = "Confirmation code"
    body = f"Ваш код подтверждения - {confirmation_code}"
    send_mail(
        subject, body, None, [email, ],
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def email(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    eml = serializer.data.get('email')
    confirm = get_random_secret_key()
    if User.objects.filter(email=eml).exists():
        User.objects.filter(email=eml).update(confirm=confirm)
    else:
        User.objects.create(email=eml, username=eml, confirm=confirm)
    send_msg(eml, confirm)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = ConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    user = get_object_or_404(User, email=email)
    if user.confirm == serializer.data.get('confirmation_code'):
        token = str(RefreshToken.for_user(user).access_token)
        return Response({'token': token}, status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'Wrong confirmation code'},
                    status=status.HTTP_400_BAD_REQUEST)
