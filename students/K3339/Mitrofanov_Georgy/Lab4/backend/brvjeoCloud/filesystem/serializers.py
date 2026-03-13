from rest_framework import serializers

from .models import File, Folder, SharedLink


class FileSerializer(serializers.ModelSerializer):
    preview_url = serializers.SerializerMethodField()
    full_url = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    file = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = File
        fields = [
            "id", "name", "size", "mime_type", "uploaded_at", "folder",
            "preview_url", "full_url", "download_url", "file"
        ]

    def build_url(self, request, path):
        return request.build_absolute_uri(path) if request else path

    def get_full_url(self, obj):
        if obj.file:
            return obj.file.url

    def get_preview_url(self, obj):
        if obj.preview_image:
            return obj.preview_image.url 

    def get_download_url(self, obj):
        request = self.context.get("request")
        url = f"/api/files/{obj.id}/download/"
        return self.build_url(request, url)


class SharedLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedLink
        fields = ['id', 'token', 'created_at', 'expires_at', 'max_downloads', 'downloads_count']


class FolderSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)
    children = serializers.SerializerMethodField()
    parent = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Folder
        fields = [ 'id', 'name', 'created_at', 'files', 'children', 'parent']

    def get_children(self, obj):
        return FolderSerializer(obj.children.all(), many=True, context=self.context).data