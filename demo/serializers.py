from rest_framework import serializers
from .models import User


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
    