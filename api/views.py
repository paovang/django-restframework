from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from demo.models import User
from demo.serializers import UserSerializer
from rest_framework import status

@api_view(['POST'])
def create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getAll(request):
    users = User.objects.all().order_by('-id')
    serializer = UserSerializer(users, many=True)
    return Response({'users': serializer.data})

@api_view(['GET'])
def getOne(request, id):
    try:
        user = User.objects.get(pk=id)
        serializer = UserSerializer(user)
        return Response({'user': serializer.data})
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=404)