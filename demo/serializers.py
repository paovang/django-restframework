from rest_framework import serializers
from .models import User, Company, CompanyUser, Role
from django.conf import settings
import os
from .utils.file import validate_image_extension
from django.core.validators import FileExtensionValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'email': {
                'validators': [],
                'error_messages': {
                    'required': 'email is required...',
                    'blank': 'email cannot be empty...',
                }
            },
            'surname': {
                'error_messages': {
                    'required': 'surname is required...',
                    'blank': 'surname cannot be empty...',
                }
            }
        }

    def __init__(self, *args, **kwargs):
        # Call the parent class' __init__ method
        super(UserSerializer, self).__init__(*args, **kwargs)
        self.method = self.context['request'].method if 'request' in self.context else None

    def validate_surname(self, value):
        if self.method in ['PUT', 'PATCH']:
            # If it's an update, ignore the current instance in the uniqueness check
            other_users = User.objects.filter(surname=value).exclude(pk=self.instance.pk)
        else:
            # For new instances, check uniqueness without excluding the current instance
            other_users = User.objects.filter(surname=value)

        if other_users.exists():
            raise serializers.ValidationError('Surname is not unique.')
        return value
        
    def validate_email(self, value):
        if self.method in ['PUT', 'PATCH']:
            # If it's an update, ignore the current instance in the uniqueness check
            other_users = User.objects.filter(email=value).exclude(pk=self.instance.pk)
        else:
            # For new instances, check uniqueness without excluding the current instance
            other_users = User.objects.filter(email=value)

        if other_users.exists():
            raise serializers.ValidationError('Email is not unique.')
        return value

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class CompanyUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), allow_null=True)
    # profile = serializers.FileField(
    #     validators=[
    #         FileExtensionValidator(allowed_extensions=['jpg', 'png', 'docx']),
    #     ],
    #     error_messages = {
    #         'required': 'Your custom error message for required profile image',
    #         'invalid_extension': 'Your file must be type: jpg, png, docx',
    #         'empty': 'Your custom error message for empty profile image',
    #     },
    # )

    class Meta:
        model = CompanyUser
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        representation['profile'] = os.getenv('BASE_URL') + representation['profile'] if representation['profile'] is not None else None
       
        # Include all fields for the related user
        user_instance = instance.user
        user_representation = UserSerializer(user_instance).data
        representation['user'] = {
            'id': user_representation['id'],
            'naeme': user_representation['name'],
            'email': user_representation['email']
        }

        # Include all fields for the related company
        company_instance = instance.company
        company_representation = CompanySerializer(company_instance).data
        representation['company'] = {
            'id': company_representation['id'],
            'name': company_representation['name'],
            'phone_number': company_representation['phone_number'],
            'address': company_representation['address']
        }

        role_instance = instance.user.roles.all()
        roles_representation = RoleSerializer(role_instance, many=True).data
        representation['user']['roles'] = roles_representation

        return representation
    