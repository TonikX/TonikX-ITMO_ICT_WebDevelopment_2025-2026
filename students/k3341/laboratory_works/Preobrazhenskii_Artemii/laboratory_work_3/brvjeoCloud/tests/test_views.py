import io
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APIClient

from brvjeoCloud.filesystem.models import File, Folder


class FileViewSetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")

        self.folder = Folder.objects.create(owner=self.user, name="folder")
        self.file = File.objects.create(
            owner=self.user,
            name="file.txt",
            size=10,
            mime_type="text/plain",
            file="file.txt",  
            updated_at=timezone.now(),
        )

    def test_list_files(self):
        url = reverse("file-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], self.file.name)

    def test_create_file(self):
        url = reverse("file-list")
        data = {"file": io.BytesIO(b"Hello World")}
        data["file"].name = "hello.txt"
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "hello.txt")

    def test_move_file(self):
        url = reverse("file-move", args=[self.file.id])
        response = self.client.post(url, {"folder_id": self.folder.id})
        self.assertEqual(response.status_code, 200)
        self.file.refresh_from_db()
        self.assertEqual(self.file.folder_id, self.folder.id)

    def test_bulk_upload(self):
        url = reverse("file-bulk-upload")
        f1 = io.BytesIO(b"file1")
        f1.name = "file1.txt"
        f2 = io.BytesIO(b"file2")
        f2.name = "file2.txt"
        response = self.client.post(url, {"files": [f1, f2]}, format="multipart")
        self.assertEqual(response.status_code, 201)
        self.assertGreaterEqual(len(response.data), 1)

    def test_share_file(self):
        url = reverse("file-share", args=[self.file.id])
        response = self.client.post(url, {"ttl_minutes": 120, "max_downloads": 10})
        self.assertEqual(response.status_code, 200)
        self.assertIn("url", response.data)


class FolderViewSetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")

        self.folder = Folder.objects.create(owner=self.user, name="folder")
        self.file = File.objects.create(
            owner=self.user,
            name="file.txt",
            size=10,
            mime_type="text/plain",
            file="file.txt",  
            updated_at=timezone.now(),
            folder=self.folder,
        )

    def test_list_folders(self):
        url = reverse("folder-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], self.folder.name)

    def test_folder_content(self):
        url = reverse("folder-content", args=[self.folder.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        files = response.data["files"]
        self.assertGreater(len(files), 0)

        self.assertEqual(files[0]["name"], self.file.name)

    def test_delete_folder_soft_deletes_files(self):
        url = reverse("folder-detail", args=[self.folder.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.file.refresh_from_db()
        self.assertIsNotNone(self.file.deleted_at)


class PublicSharedFileViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")

        self.file = File.objects.create(
            owner=self.user,
            name="file.txt",
            size=10,
            mime_type="text/plain",
            file="file.txt",  
            updated_at=timezone.now(),
        )

        self.shared_link = self.file.shared_links.create(
            expires_at=timezone.now() + timedelta(minutes=60),
            max_downloads=5,
        )

    def test_public_shared_file(self):
        url = reverse("public-file", args=[self.shared_link.token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("X-Accel-Redirect", response)

    def test_public_shared_file_expired(self):
        self.shared_link.expires_at = timezone.now() - timedelta(minutes=1)
        self.shared_link.save()
        url = reverse("public-file", args=[self.shared_link.token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_public_shared_file_max_downloads(self):
        self.shared_link.download_count = self.shared_link.max_downloads
        self.shared_link.save()
        url = reverse("public-file", args=[self.shared_link.token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)