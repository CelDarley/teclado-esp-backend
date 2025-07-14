from rest_framework import serializers
from .models import User, AccessLog, SystemConfig, Device

class DeviceSerializer(serializers.ModelSerializer):
    """Serializer para dispositivos"""
    class Meta:
        model = Device
        fields = ['id', 'name', 'ip_address', 'description', 'is_active', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    """Serializer para usuários"""
    device_name = serializers.CharField(source='device.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'device', 'device_name', 'username', 'first_name', 'last_name', 'pin', 'is_active_user', 'created_at', 'updated_at']

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
    """Serializer para logs de acesso"""
    device_name = serializers.CharField(source='device.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = AccessLog
        fields = ['id', 'device', 'device_name', 'user', 'user_name', 'access_time', 'success', 'ip_address']

class SystemConfigSerializer(serializers.ModelSerializer):
    """Serializer para configurações do sistema"""
    device_name = serializers.CharField(source='device.name', read_only=True)
    
    class Meta:
        model = SystemConfig
        fields = ['id', 'device', 'device_name', 'admin_pin', 'door_open_duration', 'max_login_attempts']

class LoginSerializer(serializers.Serializer):
    pin = serializers.CharField(max_length=4, min_length=4)
    
    def validate_pin(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("PIN deve conter apenas números")
        return value

class AccessAttemptSerializer(serializers.Serializer):
    pin = serializers.CharField(max_length=4, min_length=4)
    ip_address = serializers.IPAddressField(required=False) 