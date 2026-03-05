import io

from django.core.files import File as DjangoFile

import ffmpeg
from celery import shared_task

from brvjeoCloud.filesystem.models import File


@shared_task
def generate_preview(file_id):
    file = File.objects.get(id=file_id)
    orig_path = file.file.path

    # ----- IMAGE PREVIEW -----
    if file.mime_type.startswith("image/"):
        from PIL import Image

        image = Image.open(orig_path)
        if image.mode != "RGB":
            image = image.convert("RGB")

        image.thumbnail((300, 300))

        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        buf.seek(0)

        file.preview_image.save(f"{file_id}.jpg", DjangoFile(buf), save=True)
        return

    # ----- VIDEO PREVIEW -----
    if file.mime_type.startswith("video/"):
        process = (
            ffmpeg
            .input(orig_path, ss=0.5)
            .filter("scale", 300, -1)
            .output("pipe:", vframes=1, format="image2", vcodec="mjpeg")
            .run(capture_stdout=True, capture_stderr=True)
        )

        stdout, stderr = process  # <— ВОТ ЭТО НУЖНО

        buf = io.BytesIO(stdout)
        file.preview_image.save(f"{file_id}.jpg", DjangoFile(buf), save=True)