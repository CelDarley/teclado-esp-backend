from rest_framework import serializers
from .models import User, AccessLog, SystemConfig

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'pin', 'is_active_user', 'created_at']
        read_only_fields = ['id', 'created_at']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'pin', 'password']
    
    def create(self, validated_data):
        # Não usar set_password, apenas salvar a senha como está
        user = User(**validated_data)
        user.save()
        return user

class AccessLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = AccessLog
        fields = ['id', 'user', 'user_name', 'access_time', 'success', 'ip_address']
        read_only_fields = ['id', 'access_time']

class SystemConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfig
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    pin = serializers.CharField(max_length=4, min_length=4)
    
    def validate_pin(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("PIN deve conter apenas números")
        return value

class AccessAttemptSerializer(serializers.Serializer):
    pin = serializers.CharField(max_length=4, min_length=4)
    ip_address = serializers.IPAddressField(required=False) 