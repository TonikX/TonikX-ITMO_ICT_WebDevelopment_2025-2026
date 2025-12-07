import os

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

import ffmpeg
from PIL import Image

from brvjeoCloud.filesystem.models import File
from brvjeoCloud.tasks import generate_preview


class GeneratePreviewTaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        image_path = os.path.join(settings.CONTENT_DIR, "test_image.jpg")
        Image.new("RGB", (640, 480), color="red").save(image_path)

        self.image_file = File.objects.create(
            owner=self.user,
            name="test_image.jpg",
            mime_type="image/jpeg",
            size=os.path.getsize(image_path),
            file="content/test_image.jpg",
            updated_at=timezone.now(),
        )
        video_path = os.path.join(settings.CONTENT_DIR, "test_video.mp4")
        (
        ffmpeg
        .input("testsrc=duration=1:size=320x240:rate=30", f="lavfi")
        .output(video_path, vcodec="libx264", pix_fmt="yuv420p", movflags="+faststart")
        .run(overwrite_output=True, quiet=True)
        )

        self.video_file = File.objects.create(
            owner=self.user,
            name="test_video.mp4",
            mime_type="video/mp4",
            size=os.path.getsize(video_path),
            file="content/test_video.mp4",
            updated_at=timezone.now(),
        )

    def test_generate_preview_image(self):
        generate_preview(self.image_file.id)
        self.image_file.refresh_from_db()
        self.assertIsNotNone(self.image_file.preview_image)
        self.assertTrue(os.path.exists(self.image_file.preview_image.path))

    def test_generate_preview_video(self):
        generate_preview(self.video_file.id)
        self.video_file.refresh_from_db()
        self.assertIsNotNone(self.video_file.preview_image)
        self.assertTrue(os.path.exists(self.video_file.preview_image.path))