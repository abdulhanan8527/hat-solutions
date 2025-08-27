# storage_backends_fallback.py
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings

class FallbackStaticStorage(FileSystemStorage):
    """
    Fallback storage for static files when Supabase is not available
    """
    def __init__(self, location=None, base_url=None):
        if location is None:
            location = os.path.join(settings.BASE_DIR, 'staticfiles')
        if base_url is None:
            base_url = '/static/'
        super().__init__(location, base_url)

class FallbackMediaStorage(FileSystemStorage):
    """
    Fallback storage for media files when Supabase is not available
    """
    def __init__(self, location=None, base_url=None):
        if location is None:
            location = os.path.join(settings.BASE_DIR, 'media')
        if base_url is None:
            base_url = '/media/'
        super().__init__(location, base_url)