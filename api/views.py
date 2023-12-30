from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from demo.models import User, Company, CompanyUser
from demo.serializers import UserSerializer, CompanyUserSerializer, UploadedFileSerializer
from .response_format import ResponseFormat
from demo.response_format.format_com_user import ResponseFormatComPanyUser
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from datetime import datetime

class UserView(APIView):
    response_format = ResponseFormat()
    format_com_user = ResponseFormatComPanyUser()
    paginator = PageNumberPagination()

    # def post(self, request, *args, **kwargs):
    #     try:
    #         # Extract data from the request
    #         user_id = request.data.get('user_id')
    #         company_id = request.data.get('company_id')
    #         profile = request.data.get('profile')

    #         # Fetch User and Company instances
    #         user = User.objects.get(pk=user_id)
    #         company = Company.objects.get(pk=company_id)
            
    #         # Create CompanyUser instance
    #         company_user = CompanyUser.objects.create(user=user, company=company, profile=profile)

    #         # Serialize the created CompanyUser instance
    #         serializer = CompanyUserSerializer(company_user)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     except User.DoesNotExist:
    #         return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    #     except Company.DoesNotExist:
    #         return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
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


    # Company Users
    @api_view(['POST'])
    def company_user_create(request):
        try:
            # Extract data from the request
            user_id = request.data.get('user_id')
            company_id = request.data.get('company_id')
            profile = request.data.get('profile')

            # Fetch User and Company instances
            user = User.objects.get(pk=user_id)
            company = Company.objects.get(pk=company_id)
            
            # Create CompanyUser instance
            company_user = CompanyUser.objects.create(user=user, company=company, profile=profile)

            # Serialize the created CompanyUser instance
            serializer = CompanyUserSerializer(company_user)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @api_view(['GET'])
    def company_user_get_all(request):
        try:
            # Get per_page or page_size from the request
            per_page = int(request.GET.get('per_page', 10))  # Default to 10 if not specified
            UserView.paginator.page_size = per_page
            name_filter = request.GET.get('name', '')

            #  Get key start_date and end_date from the request
            start_date_str, end_date_str = request.GET.get('start_date', ''), request.GET.get('end_date', '')

            #  Convert the date strings to datetime objects
            start_date, end_date = (
                datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None,
                datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None
            )

            # filter Company User
            company_users = CompanyUser.objects.prefetch_related('user', 'company').filter(
                Q(user__name__icontains=name_filter) | Q(user__surname__icontains=name_filter),
                (Q(user__created_at__date__range=(start_date, end_date)) if start_date and end_date else Q())
            ).order_by('-id')

            # Paginate the queryset
            result_paginate = UserView.paginator.paginate_queryset(company_users, request)
            serializer = CompanyUserSerializer(result_paginate, many=True)
    
            formatted_items = [UserView.format_com_user.to_format(item) for item in serializer.data]

            response_data = {
                'status': status.HTTP_200_OK,
                'message': 'successfully retrieved users',
                'data': formatted_items,
                'count': UserView.paginator.page.paginator.count,
                'next': UserView.paginator.get_next_link(),
                'previous': UserView.paginator.get_previous_link()
            }

            return Response(response_data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @api_view(['POST'])
    def upload_file(request):
        file_serializer = UploadedFileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)