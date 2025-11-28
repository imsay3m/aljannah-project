from .models import SiteConfiguration


def site_configuration(request):
    """
    Returns the singleton SiteConfiguration object to the template context.
    Usage in templates: {{ site_config.head_teacher_phone }}
    """
    try:
        config = SiteConfiguration.objects.first()
    except:
        config = None

    return {
        "site_config": config,
    }
