from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator

class Device(models.Model):
    """Modelo de dispositivo"""
    name = models.CharField(max_length=100, unique=True, help_text='Nome do dispositivo')
    ip_address = models.GenericIPAddressField(unique=True, help_text='Endereço IP do dispositivo')
    description = models.TextField(blank=True, null=True, help_text='Descrição do dispositivo')
    is_active = models.BooleanField(default=True, help_text='Dispositivo ativo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.ip_address})"

class User(models.Model):
    """Modelo de usuário customizado"""
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='users', help_text='Dispositivo ao qual o usuário pertence', null=True, blank=True)
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    pin = models.CharField(
        max_length=4,
        validators=[
            MinLengthValidator(4, 'PIN deve ter exatamente 4 dígitos'),
            RegexValidator(r'^\d{4}$', 'PIN deve conter apenas números')
        ],
        help_text='PIN de 4 dígitos para acesso'
    )
    password = models.CharField(max_length=128)
    is_active_user = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        unique_together = ['device', 'username']  # Username único por dispositivo

    def __str__(self):
        return f"{self.username} - {self.device.name if self.device else 'Sem dispositivo'} - PIN: {self.pin}"

class AccessLog(models.Model):
    """Histórico de acessos"""
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='access_logs', help_text='Dispositivo onde ocorreu o acesso', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='access_logs', null=True, blank=True)
    access_time = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Log de Acesso'
        verbose_name_plural = 'Logs de Acesso'
        ordering = ['-access_time']

    def __str__(self):
        status = "✅ Acesso" if self.success else "❌ Negado"
        device_name = self.device.name if self.device else 'Dispositivo Desconhecido'
        return f"{device_name} - {self.user.username if self.user else 'Desconhecido'} - {self.access_time.strftime('%d/%m/%Y %H:%M')} - {status}"

class SystemConfig(models.Model):
    """Configurações do sistema"""
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='configs', help_text='Dispositivo da configuração', null=True, blank=True)
    admin_pin = models.CharField(
        max_length=4,
        default='8729',
        validators=[
            MinLengthValidator(4, 'PIN deve ter exatamente 4 dígitos'),
            RegexValidator(r'^\d{4}$', 'PIN deve conter apenas números')
        ]
    )
    door_open_duration = models.IntegerField(
        default=5,
        help_text='Duração da abertura da porta em segundos'
    )
    max_login_attempts = models.IntegerField(
        default=3,
        help_text='Número máximo de tentativas de login'
    )
    
    class Meta:
        verbose_name = 'Configuração do Sistema'
        verbose_name_plural = 'Configurações do Sistema'
        unique_together = ['device']  # Uma configuração por dispositivo

    def __str__(self):
        device_name = self.device.name if self.device else 'Dispositivo Desconhecido'
        return f"Configuração do {device_name} - Admin PIN: {self.admin_pin}"
