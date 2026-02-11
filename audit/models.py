from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Audit(models.Model):
    
    ACTION_CHOICES = (
        ('CREATE', 'Criou'),
        ('UPDATE', 'Atualizou'),
        ('DELETE', 'Deletou'),
        ('LOGIN',  'Login'),
        ('LOGOUT', 'Saindo'),
        ('DOWNLOAD', 'Baixou'),
    )
    
    dono = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, verbose_name="Usuário"      )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    cache_data = models.JSONField('Dados armazenados', null=True, blank=True)
    action = models.CharField('Ação', max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField('Endereço IP', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Regristro de Auditoria'
        verbose_name_plural = 'Registros de auditoria'
        ordering = ['-timestamp']
    
    def __str__(self):
        data_local = timezone.localtime(self.timestamp)
        data_formatada = data_local.strftime('%d/%m/%Y %H:%M:%S')
        return f"{self.dono} - executou a ação de: {self.action} - na data/hora: {data_formatada} - o arquivo/pasta: '{self.content_object}'"
    
    def delete(self, *args, **kwargs):
        if not kwargs.get('force', False):
            raise PermissionError("Nenhum log de auditoria pode ser apagado.")
        super().delete(*args, **kwargs)
        