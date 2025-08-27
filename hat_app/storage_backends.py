import os
from django.core.files.base import ContentFile
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.core.files.storage import Storage
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "hat-solutions")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class SupabaseMediaStorage(Storage):
    """For MEDIA files"""
    location = "media"

    def _save(self, name, content):
        path = f"{self.location}/{name}"
        data = content.read()
        print(f"🔹 Uploading MEDIA {path} to Supabase...")
        res = supabase.storage.from_(SUPABASE_BUCKET).upload(path, data, {"upsert": True})
        if isinstance(res, dict) and res.get("error"):
            raise Exception(f"Supabase upload error: {res['error']}")
        return path

    def _open(self, name, mode="rb"):
        res = supabase.storage.from_(SUPABASE_BUCKET).download(f"{self.location}/{name}")
        if isinstance(res, bytes):
            return ContentFile(res)
        raise Exception("Failed to download file from Supabase")

    def url(self, name):
        return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{self.location}/{name}"

    def exists(self, name):
        try:
            files = supabase.storage.from_(SUPABASE_BUCKET).list(self.location)
            return any(f["name"] == name for f in files)
        except Exception:
            return False
        

class SupabaseStaticStorage(ManifestStaticFilesStorage):
    location = "static"

    def _save(self, name, content):
        path = f"{self.location}/{name}"
        data = content.read()
        print(f"🔹 Uploading STATIC {path} to Supabase...")

        res = supabase.storage.from_(SUPABASE_BUCKET).upload(
            path, data, {"upsert": True}
        )
        if isinstance(res, dict) and res.get("error"):
            raise Exception(f"Supabase upload error: {res['error']}")
        return path

    def url(self, name):
        return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{self.location}/{name}"

    def post_process(self, paths, dry_run=False, **options):
        # Force upload every file during collectstatic
        for name, hashed_name, processed in super().post_process(paths, dry_run, **options):
            full_path = self.path(name)
            with open(full_path, "rb") as f:
                self._save(name, f)
            yield name, hashed_name, processed


# class SupabaseStaticStorage(ManifestStaticFilesStorage):
#     """For STATIC files (subclass ManifestStaticFilesStorage so Django uses it)"""
#     location = "static"

#     def _save(self, name, content):
#         path = f"{self.location}/{name}"
#         data = content.read()
#         print(f"🔹 Uploading STATIC {path} to Supabase...")
#         res = supabase.storage.from_(SUPABASE_BUCKET).upload(path, data, {"upsert": True})
#         if isinstance(res, dict) and res.get("error"):
#             raise Exception(f"Supabase upload error: {res['error']}")
#         return path

#     def url(self, name):
#         return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{self.location}/{name}"
