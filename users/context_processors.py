from .models import AuthSettings

def auth_settings(request):
    return {
        'auth_settings': AuthSettings.objects.first()
    }
