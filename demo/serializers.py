from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'email': {'validators': []},
            'surname': {'validators': []},
        }

    def validate_surname(self, value):
        print("Validating surname:", value)
        if not value.strip():
            raise serializers.ValidationError('Surname should not be empty or contain only whitespace.')
        if User.objects.filter(surname=value).exists():
            raise serializers.ValidationError('Surname is not unique.')
        return value
        
    def validate_email(self, value):
        print("Validating Email:", value)
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email is not unique.')
        return value

    