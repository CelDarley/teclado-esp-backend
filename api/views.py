from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User, AccessLog
from .serializers import UserSerializer, AccessLogSerializer
import json

@api_view(['GET'])
def status_view(request):
    """Endpoint de teste para verificar se a API está funcionando"""
    return Response({
        'status': 'ok',
        'message': 'API funcionando corretamente'
    })

@api_view(['POST'])
def login_view(request):
    """View para login com PIN"""
    try:
        data = json.loads(request.body)
        pin = data.get('pin')
        
        if not pin:
            return Response({
                'success': False,
                'message': 'PIN não fornecido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar se é o PIN admin padrão
        if pin == '8729':
            return Response({
                'success': True,
                'message': 'Login admin realizado com sucesso',
                'user_type': 'admin'
            }, status=status.HTTP_200_OK)
        
        # Verificar se existe um usuário com este PIN
        try:
            user = User.objects.get(pin=pin)
            return Response({
                'success': True,
                'message': f'Login realizado com sucesso para {user.name}',
                'user_type': 'user',
                'user_name': user.name
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'PIN inválido'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
    except json.JSONDecodeError:
        return Response({
            'success': False,
            'message': 'JSON inválido'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def access_verify_view(request):
    """View para verificação de acesso (ESP32)"""
    try:
        data = json.loads(request.body)
        pin = data.get('pin')
        
        if not pin:
            return Response({
                'success': False,
                'message': 'PIN não fornecido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar se é o PIN admin padrão
        if pin == '8729':
            # Registrar log de acesso
            AccessLog.objects.create(
                user=None,
                success=True,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return Response({
                'success': True,
                'message': 'Acesso admin autorizado',
                'access_granted': True
            }, status=status.HTTP_200_OK)
        
        # Verificar se existe um usuário com este PIN
        user = User.objects.filter(pin=pin).first()
        if user:
            # Registrar log de acesso
            AccessLog.objects.create(
                user=user,
                success=True,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return Response({
                'success': True,
                'message': f'Acesso autorizado para {user.username}',
                'access_granted': True,
                'user_name': user.username
            }, status=status.HTTP_200_OK)
        else:
            # Registrar log de acesso negado
            AccessLog.objects.create(
                user=None,
                success=False,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return Response({
                'success': False,
                'message': 'PIN inválido - Acesso negado',
                'access_granted': False
            }, status=status.HTTP_401_UNAUTHORIZED)
            
    except json.JSONDecodeError:
        return Response({
            'success': False,
            'message': 'JSON inválido'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def users_view(request):
    """Listar todos os usuários"""
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_user_view(request):
    """Criar novo usuário"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def logs_view(request):
    """Listar logs de acesso"""
    logs = AccessLog.objects.all().order_by('-timestamp')
    serializer = AccessLogSerializer(logs, many=True)
    return Response(serializer.data)
