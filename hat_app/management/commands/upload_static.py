# hat_app/management/commands/upload_static.py
import os
from django.core.management.base import BaseCommand
from django.contrib.staticfiles import finders
from django.core.files.storage import default_storage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Upload static files to Supabase with fallback'

    def handle(self, *args, **options):
        # Check if Supabase is configured
        if not all([settings.SUPABASE_URL, settings.SUPABASE_KEY]):
            self.stdout.write(
                self.style.WARNING('Supabase not configured. Using local static files.')
            )
            return
        
        # Use the staticfiles finder to locate all static files
        static_files = []
        for finder in settings.STATICFILES_FINDERS:
            if finder == 'django.contrib.staticfiles.finders.AppDirectoriesFinder':
                for app in settings.INSTALLED_APPS:
                    app_path = os.path.join(settings.BASE_DIR, app, 'static')
                    if os.path.exists(app_path):
                        for root, dirs, files in os.walk(app_path):
                            for file in files:
                                static_files.append(os.path.relpath(os.path.join(root, file), app_path))
            
            elif finder == 'django.contrib.staticfiles.finders.FileSystemFinder':
                for static_dir in getattr(settings, 'STATICFILES_DIRS', []):
                    if os.path.exists(static_dir):
                        for root, dirs, files in os.walk(static_dir):
                            for file in files:
                                static_files.append(os.path.relpath(os.path.join(root, file), static_dir))

        # Upload each static file with error handling
        successful_uploads = 0
        for static_file in static_files:
            try:
                file_path = finders.find(static_file)
                if file_path:
                    with open(file_path, 'rb') as f:
                        default_storage.save(static_file, f)
                        successful_uploads += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'Uploaded {static_file}')
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Could not find {static_file}')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to upload {static_file}: {str(e)}')
                )

        if successful_uploads > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully uploaded {successful_uploads} files to Supabase')
            )
        else:
            self.stdout.write(
                self.style.WARNING('No files were uploaded to Supabase. Using fallback storage.')
            )