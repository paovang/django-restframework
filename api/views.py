from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from demo.models import User
from demo.serializers import UserSerializer
from .response_format import ResponseFormat

class UserView(APIView):
    response_format = ResponseFormat()

    @api_view(['POST'])
    def create(request):
        try:
            serializer = UserSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @api_view(['PUT'])
    def update(request, id):
        try:
            user = get_object_or_404(User, pk=id)
            serializer = UserSerializer(user, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @api_view(['GET'])
    def get_all(request):
        users = User.objects.all().order_by('-id')
        serializer = UserSerializer(users, many=True)
        formatted_users = [UserView.response_format.to_format(item) for item in serializer.data]

        response_data = {
            'status': status.HTTP_200_OK,
            'message': 'successfully retrieved users',
            'data': formatted_users
        }

        return Response(response_data)

    @api_view(['GET'])
    def get_one(request, id):
        user = get_object_or_404(User, pk=id)
        serializer = UserSerializer(user)

        response_data = {
            'status': status.HTTP_200_OK,
            'message': 'successfully retrieved users',
            'data': UserView.response_format.to_format(serializer.data)
        }

        return Response(response_data)