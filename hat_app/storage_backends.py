from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "hat-solutions")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class SupabaseStaticStorage(Storage):
    """Storage for static files (CSS, JS, Admin assets)."""
    location = "static"

    def _save(self, name, content):
        path = f"{self.location}/{name}"
        data = content.read()
        res = supabase.storage.from_(SUPABASE_BUCKET).upload(path, data, {"upsert": True})
        if "error" in res:
            raise Exception(f"Supabase upload error: {res['error']}")
        return path

    def url(self, name):
        return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{self.location}/{name}"


class SupabaseMediaStorage(Storage):
    """Storage for uploaded media (user files, portfolio images)."""
    location = "media"

    def _save(self, name, content):
        path = f"{self.location}/{name}"
        data = content.read()
        res = supabase.storage.from_(SUPABASE_BUCKET).upload(path, data, {"upsert": True})
        if "error" in res:
            raise Exception(f"Supabase upload error: {res['error']}")
        return path

    def url(self, name):
        return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{self.location}/{name}"
