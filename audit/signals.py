import json
from audit.middleware import get_current_request
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from audit.models import Audit
from vault.models import File, Folder
from django.core.serializers.json import DjangoJSONEncoder

def get_ip_user(request):
    if not request: return None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def save_log(instance, action):
    request = get_current_request()
    
    if not request:
        return 
    
    user = getattr(request, 'user', None)
    
    if not user or not user.is_authenticated:
        return 
    
    ip_user = get_ip_user(request=request)
    
    dados_limpos = {} 

    try:
        dados = model_to_dict(instance=instance)
        if hasattr(instance, 'file') and instance.file:
            dados['file'] = str(instance.file)
        
        dados_limpos = json.loads(
            json.dumps(
                dados, cls=DjangoJSONEncoder
            )
        )        
        
    except Exception as e:
        dados_limpos = {"error": str(e)}
        
    Audit.objects.create(
        action=action,
        content_object=instance,
        dono=user,
        cache_data=dados_limpos,
        ip_address=ip_user,
    )

@receiver(post_save, sender=File)
@receiver(post_save, sender=Folder)
def post_save(sender, instance, created, **kwargs):
    if created:
        action = 'CRIOU'
    else: 
        action = 'EDITOU'
    save_log(instance=instance, action=action)
    
@receiver(post_delete, sender=File)
@receiver(post_delete, sender=Folder)
def post_delete(sender, instance, **kwargs):
    save_log(instance=instance, action='DELETOU')
    