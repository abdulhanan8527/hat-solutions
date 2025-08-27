import os
from django.core.management.base import BaseCommand
from django.contrib.staticfiles import finders
from django.core.files.storage import default_storage
from django.conf import settings

class Command(BaseCommand):
    help = 'Upload static files to Supabase'

    def handle(self, *args, **options):
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
                for static_dir in settings.STATICFILES_DIRS:
                    if os.path.exists(static_dir):
                        for root, dirs, files in os.walk(static_dir):
                            for file in files:
                                static_files.append(os.path.relpath(os.path.join(root, file), static_dir))

        # Upload each static file
        for static_file in static_files:
            with open(finders.find(static_file), 'rb') as f:
                default_storage.save(static_file, f)
                self.stdout.write(self.style.SUCCESS(f'Uploaded {static_file}'))

        self.stdout.write(self.style.SUCCESS('All static files uploaded to Supabase'))