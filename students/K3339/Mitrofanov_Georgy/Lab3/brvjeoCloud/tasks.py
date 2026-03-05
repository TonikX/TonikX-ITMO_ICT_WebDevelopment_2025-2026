import os

from django.conf import settings

import ffmpeg
from celery import shared_task
from PIL import Image

from brvjeoCloud.filesystem.models import File


@shared_task
def generate_preview(file_id):
    file = File.objects.get(id=file_id)
    orig_path = file.file.path
    preview_path = os.path.join(settings.PREVIEWS_DIR, f"{file_id}_preview.jpg")

    if file.mime_type.startswith('image/'):
        image = Image.open(orig_path)
        image.thumbnail((300, 300))
        image.save(preview_path)
    elif file.mime_type.startswith('video/'):
        ffmpeg.input(orig_path, ss=0.5)\
              .filter('scale', 300, -1)\
              .output(preview_path, vframes=1)\
              .run(overwrite_output=True, quiet=True)

    file.preview_image.name = os.path.relpath(preview_path, settings.MEDIA_ROOT)
    file.save()