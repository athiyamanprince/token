from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def login(req):
    user = get_object_or_404(User, username=req.data['username'])
    if not user.check_password(req.data['password']):
        return Response({"details":"Not found."},status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serializer=UserSerializer(instance=user)
    return Response({"token":token.key,"user":serializer.data})
    # return Response({})

@api_view(['POST'])
def signup(req):
    serializer = UserSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=req.data['username'])
        user.set_password(req.data['password'])
        user.save()
        token=Token.objects.create(user=user)
        return Response({"token":token.key,"user":serializer.data})
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(req):
    return Response("passed for {}".format(req.user.email))