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

@api_view(['GET'])
def check_auth_view(request):
    """Verificar se o usuário está autenticado"""
    # Por enquanto, sempre retorna que está logado
    # Você pode implementar verificação de token aqui
    return Response({
        'success': True,
        'message': 'Usuário autenticado',
        'user_type': 'admin'  # ou 'user' baseado no token
    })

@api_view(['POST'])
def login_view(request):
    """View para login com usuário e senha"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return Response({
                'success': False,
                'message': 'Usuário e senha são obrigatórios'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar se é o admin padrão
        if username == 'admin' and password == 'admin123':
            return Response({
                'success': True,
                'message': 'Login admin realizado com sucesso',
                'user_type': 'admin'
            }, status=status.HTTP_200_OK)
        
        # Verificar se existe um usuário com estas credenciais
        try:
            user = User.objects.get(username=username)  # type: ignore
            # Aqui você pode adicionar verificação de senha se necessário
            # Por enquanto, vamos aceitar qualquer senha para usuários existentes
            return Response({
                'success': True,
                'message': f'Login realizado com sucesso para {user.first_name}',
                'user_type': 'user',
                'user_name': user.first_name
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:  # type: ignore
            return Response({
                'success': False,
                'message': 'Usuário ou senha inválidos'
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
            AccessLog.objects.create(  # type: ignore
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
        user = User.objects.filter(pin=pin).first()  # type: ignore
        if user:
            # Registrar log de acesso
            AccessLog.objects.create(  # type: ignore
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
            AccessLog.objects.create(  # type: ignore
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
    users = User.objects.all()  # type: ignore
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_user_view(request):
    """Criar novo usuário"""
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # type: ignore
            username = request.data.get('username', '')
            return Response({
                'success': True,
                'message': f'Usuário {username} criado com sucesso',
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            # Verificar se é erro de username duplicado
            if 'username' in serializer.errors:
                username = request.data.get('username', '')
                return Response({
                    'success': False,
                    'message': f'Usuário "{username}" já existe. Use um nome de usuário diferente.',
                    'error_type': 'duplicate_username'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'success': False,
                    'message': 'Dados inválidos. Verifique os campos obrigatórios.',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_user_view(request, user_id):
    """Excluir usuário por ID"""
    try:
        user = User.objects.get(id=user_id)  # type: ignore
        user.delete()
        return Response({
            'success': True,
            'message': f'Usuário {user.username} excluído com sucesso'
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:  # type: ignore
        return Response({
            'success': False,
            'message': 'Usuário não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Erro ao excluir usuário: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def logs_view(request):
    """Listar logs de acesso"""
    logs = AccessLog.objects.all().order_by('-access_time')  # type: ignore
    serializer = AccessLogSerializer(logs, many=True)
    return Response(serializer.data)
