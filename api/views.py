from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def test_connection(request):
    """
    Endpoint de teste para verificar a comunicação entre Vue e Django
    """
    return Response({
        'message': 'Conexão com Django funcionando!',
        'status': 'success',
        'data': {
            'backend': 'Django REST Framework',
            'frontend': 'Vue 3 + TypeScript',
            'project': 'Teclado ESP32'
        }
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def keyboard_status(request):
    """
    Endpoint para obter o status do teclado
    """
    return Response({
        'connected': True,
        'device': 'ESP32 Keyboard',
        'battery': 85,
        'rgb_enabled': True,
        'current_profile': 'default'
    }, status=status.HTTP_200_OK) 