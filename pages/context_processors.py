from config.site_config import SITE


def site_config(request):
    """Make personal site settings available in every template as `site`."""
    site = dict(SITE)
    # Honest placeholder: never invent a name, show a clear marker instead.
    site['display_name'] = SITE['owner_name'] or '[Your Name]'
    return {'site': site}