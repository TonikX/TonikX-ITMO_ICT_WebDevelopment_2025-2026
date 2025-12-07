from rest_framework import serializers

from .models import File, Folder, SharedLink


class FileSerializer(serializers.ModelSerializer):
    preview_url = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    file = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = File
        fields = [ "id", "name", "size", "mime_type", "uploaded_at", "preview_url", "download_url", "file", "collaborators"]
    
    def get_preview_url(self, obj):
        request = self.context.get("request")
        if obj.preview_image:
            return request.build_absolute_uri(f"/api/files/{obj.id}/preview/")
        return None

    def get_download_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(f"/api/files/{obj.id}/download/")
    

class SharedLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedLink
        fields = ['id', 'token', 'created_at', 'expires_at', 'max_downloads', 'downloads_count']


class FolderSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = [ 'id', 'name', 'created_at', 'files', 'children']

    def get_children(self, obj):
        return FolderSerializer(obj.children.all(), many=True, context=self.context).data