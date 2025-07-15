from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User, AccessLog, Device, SystemConfig
from .serializers import UserSerializer, AccessLogSerializer, DeviceSerializer, SystemConfigSerializer
import json
from django.utils import timezone

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
        device_ip = request.META.get('REMOTE_ADDR')
        
        if not pin:
            return Response({
                'success': False,
                'message': 'PIN não fornecido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Encontrar o dispositivo pelo IP
        device = Device.objects.filter(ip_address=device_ip, is_active=True).first()  # type: ignore
        if not device:
            return Response({
                'success': False,
                'message': 'Dispositivo não encontrado ou inativo'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Verificar se é o PIN admin padrão do dispositivo
        config = SystemConfig.objects.filter(device=device).first()  # type: ignore
        admin_pin = config.admin_pin if config else '8729'
        
        if pin == admin_pin:
            # Registrar log de acesso
            AccessLog.objects.create(  # type: ignore
                device=device,
                user=None,
                success=True,
                ip_address=device_ip
            )
            return Response({
                'success': True,
                'message': 'Acesso admin autorizado',
                'access_granted': True
            }, status=status.HTTP_200_OK)
        
        # Verificar se existe um usuário com este PIN no dispositivo
        user = User.objects.filter(device=device, pin=pin).first()  # type: ignore
        if user:
            # Registrar log de acesso
            AccessLog.objects.create(  # type: ignore
                device=device,
                user=user,
                success=True,
                ip_address=device_ip
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
                device=device,
                user=None,
                success=False,
                ip_address=device_ip
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

# Device views
@api_view(['GET'])
def devices_view(request):
    """Listar todos os dispositivos"""
    devices = Device.objects.all()  # type: ignore
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_device_view(request):
    """Criar novo dispositivo"""
    try:
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            device = serializer.save()  # type: ignore
            
            # Criar configuração padrão para o dispositivo
            SystemConfig.objects.create(  # type: ignore
                device=device,
                admin_pin='8729',
                door_open_duration=5,
                max_login_attempts=3
            )
            
            return Response({
                'success': True,
                'message': f'Dispositivo {device.name} criado com sucesso',  # type: ignore
                'device': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            # Verificar se é erro de nome duplicado
            if 'name' in serializer.errors:
                name = request.data.get('name', '')
                return Response({
                    'success': False,
                    'message': f'Dispositivo "{name}" já existe. Use um nome diferente.',
                    'error_type': 'duplicate_name'
                }, status=status.HTTP_400_BAD_REQUEST)
            elif 'ip_address' in serializer.errors:
                ip = request.data.get('ip_address', '')
                return Response({
                    'success': False,
                    'message': f'IP "{ip}" já está em uso. Use um IP diferente.',
                    'error_type': 'duplicate_ip'
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
def delete_device_view(request, device_id):
    """Excluir dispositivo por ID"""
    try:
        device = Device.objects.get(id=device_id)  # type: ignore
        device_name = device.name
        device.delete()
        return Response({
            'success': True,
            'message': f'Dispositivo {device_name} excluído com sucesso'
        }, status=status.HTTP_200_OK)
    except Device.DoesNotExist:  # type: ignore
        return Response({
            'success': False,
            'message': 'Dispositivo não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Erro ao excluir dispositivo: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
def update_device_ip_view(request, device_id):
    """Atualizar o IP de um dispositivo (temporário para manutenção)"""
    try:
        device = Device.objects.get(id=device_id)  # type: ignore
        new_ip = request.data.get('ip_address')
        if not new_ip:
            return Response({'success': False, 'message': 'ip_address é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        device.ip_address = new_ip
        device.save()
        return Response({'success': True, 'message': f'IP do dispositivo {device.name} atualizado para {new_ip}'})
    except Device.DoesNotExist:  # type: ignore
        return Response({'success': False, 'message': 'Dispositivo não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': f'Erro ao atualizar IP: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# User views (updated for devices)
@api_view(['GET'])
def users_view(request):
    """Listar usuários de um dispositivo específico"""
    device_id = request.GET.get('device_id')
    if not device_id:
        return Response({
            'success': False,
            'message': 'device_id é obrigatório'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        users = User.objects.filter(device_id=device_id)  # type: ignore
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Erro ao listar usuários: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                    'message': f'Usuário "{username}" já existe neste dispositivo. Use um nome de usuário diferente.',
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
    """Listar logs de acesso de um dispositivo específico"""
    device_id = request.GET.get('device_id')
    if not device_id:
        return Response({
            'success': False,
            'message': 'device_id é obrigatório'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        logs = AccessLog.objects.filter(device_id=device_id).order_by('-access_time')  # type: ignore
        serializer = AccessLogSerializer(logs, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Erro ao listar logs: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def trigger_device_view(request, device_id):
    """Acionar dispositivo (simular acesso com PIN correto)"""
    try:
        # Verificar se o dispositivo existe
        device = Device.objects.get(id=device_id)  # type: ignore
        if not device.is_active:
            return Response({
                'success': False,
                'message': 'Dispositivo inativo'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Obter IP do cliente (ou usar um IP padrão para simulação)
        client_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        
        # Registrar log de acesso simulado (como se fosse admin)
        AccessLog.objects.create(  # type: ignore
            device=device,
            user=None,
            success=True,
            ip_address=client_ip,
            access_time=timezone.now()
        )
        
        return Response({
            'success': True,
            'message': f'Dispositivo {device.name} acionado com sucesso',
            'device_name': device.name,
            'access_granted': True
        }, status=status.HTTP_200_OK)
        
    except Device.DoesNotExist:  # type: ignore
        return Response({
            'success': False,
            'message': 'Dispositivo não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Erro ao acionar dispositivo: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
