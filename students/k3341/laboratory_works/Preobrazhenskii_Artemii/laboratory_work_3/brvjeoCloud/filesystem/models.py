import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


User = get_user_model()


class Folder(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="folders")
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'parent', 'name')
        ordering = ["created_at"]
    
    def __str__(self):
        return self.name
    
class File(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    folder = models.ForeignKey(Folder, null=True, blank=True, on_delete=models.SET_NULL, related_name="files")
    file = models.FileField(upload_to='content/')
    size = models.BigIntegerField()
    mime_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True) 
    preview_image = models.ImageField(upload_to="previews/", null=True, blank=True)
    duration_ms = models.BigIntegerField(null=True, blank=True)
    collaborators = models.ManyToManyField(User, related_name="shared_files", blank=True)
    
    def __str__(self):
        return self.name

class SharedLink(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="shared_links")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    max_downloads = models.PositiveIntegerField(null=True, blank=True)
    download_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.token

    def is_expired(self):
        if self.expires_at and timezone.now() > self.expires_at:
            return True
        if self.max_downloads is not None and self.download_count >= self.max_downloads:
            return True
        return False

    def increment_download(self):
        self.download_count += 1
        self.save()

