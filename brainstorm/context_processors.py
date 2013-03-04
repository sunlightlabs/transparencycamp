from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME


def brainstorm(request):
    ctx = {
        'DISQUS_SHORTNAME': getattr(settings, 'DISQUS_SHORTNAME'),
        'BRAINSTORM_USE_DISQUS': getattr(settings, 'BRAINSTORM_USE_DISQUS'),
        'BRAINSTORM_LOGIN_OPTIONS': getattr(settings, 'BRAINSTORM_LOGIN_OPTIONS'),
        'REDIRECT_FIELD_NAME': REDIRECT_FIELD_NAME,
    }

    return ctx
