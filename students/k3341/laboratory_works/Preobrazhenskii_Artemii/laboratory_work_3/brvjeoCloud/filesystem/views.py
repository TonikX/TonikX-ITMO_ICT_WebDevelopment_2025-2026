from urllib.parse import quote

from django.conf import settings
from django.db import transaction
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import File, Folder, SharedLink
from .permissions import IsOwner
from .serializers import FileSerializer, FolderSerializer


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return File.objects.filter(owner=self.request.user, deleted_at__isnull=True)
    
    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()

    def get_parser_classes(self):
        if getattr(self, "action", None) in ("create", "bulk_upload"):
            return [MultiPartParser, FormParser]
        return [JSONParser]
    
    @swagger_auto_schema(
        operation_description="Загрузка файла",
        manual_parameters=[],
        request_body=None,
        consumes=["multipart/form-data"],
        responses={201: FileSerializer()},
    )
    def create(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({'error': 'Файл не передан'}, status=status.HTTP_400_BAD_REQUEST)
        
        if uploaded_file.size > settings.MAX_FILE_UPLOAD_MB * 1024 * 1024:
            return Response({'error': 'Размер файла превышает допустимый'}, status=status.HTTP_400_BAD_REQUEST)
        
        if uploaded_file.content_type not in settings.ALLOWED_FILE_MIME_TYPE:
            return Response({'error': 'Недопустимый тип файла'}, status=status.HTTP_400_BAD_REQUEST)
        
        file_obj = File.objects.create(
            owner=request.user,
            name=uploaded_file.name,
            size=uploaded_file.size,
            mime_type=uploaded_file.content_type,
            file=uploaded_file  
        )

        serializer = self.get_serializer(file_obj, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        file_obj = self.get_object()
        file_path = file_obj.file.path
        filename = quote(file_obj.name)
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
        response['Content-Type'] = file_obj.mime_type or 'application/octet-stream'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    @action(detail=True)
    def preview(self, request, pk=None):
        file_obj = self.get_object()
        if not file_obj.preview_image:
            return Response({'error': 'Не удалось загрузить превью'})
        
        internal_path = '/protected-media/' + quote(file_obj.preview_image.name)  
        response = HttpResponse()
        response['Content-Type'] = 'image/jpeg'
        response['X-Accel-Redirect'] = internal_path
        return response
    
    @action(detail=True, methods=['post'])
    def move(self, request, pk=None):
        file_obj = self.get_object()
        folder_id = request.data.get('folder_id')

        if not folder_id:
            return Response({'message': 'Не указан folder_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        file_obj.folder_id = folder_id
        file_obj.save()
        return Response({'message': f'Файл {file_obj.name} перемещен'})
    
    @swagger_auto_schema(
        consumes=["multipart/form-data"],
        request_body=None,
        responses={201: FileSerializer(many=True)},
    )
    @transaction.atomic
    @action(detail=False, methods=['post'])
    def bulk_upload(self, request):
        files = request.FILES.getlist('files')
        uploaded_files = []

        for uploaded_file in files:
            file_obj = File.objects.create(
                owner=request.user,
                name=uploaded_file.name,
                size=uploaded_file.size,
                mime_type=uploaded_file.content_type,
                file=uploaded_file  
            )
            uploaded_files.append(file_obj)

        serializer = self.get_serializer(uploaded_files, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        file_obj = self.get_object()
        ttl_minutes = int(request.data.get('ttl_minutes', 60))
        shared_link = file_obj.shared_links.create(
            expires_at=timezone.now() + timezone.timedelta(minutes=ttl_minutes),
            max_downloads=request.data.get('max_downloads', None)
        )
        url = request.build_absolute_uri(f'/p/{shared_link.token}/')
        return Response({'url': url})


class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Folder.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    @transaction.atomic
    def perform_destroy(self, instance):
        files = File.objects.filter(folder=instance, deleted_at__isnull=True)
        files.update(deleted_at=timezone.now())
        instance.delete()
    
    @action(detail=True)
    def content(self, request, pk=None):
        folder = self.get_object()
        subfolders = Folder.objects.filter(parent=folder, owner=request.user)
        files = File.objects.filter(owner=request.user, folder=folder, deleted_at__isnull=True)
        folder_serializer = FolderSerializer(subfolders, many=True, context={'request': request})
        file_serializer = FileSerializer(files, many=True, context={'request': request})
        return Response({
            "folders": folder_serializer.data,
            "files": file_serializer.data
        })


class PublicSharedFileView(APIView):
    def get(self, request, token):
        shared_link = get_object_or_404(SharedLink, token=token)
        if shared_link.is_expired():
            return Response({'error': 'Ссылка недействительна или истекла'}, status=status.HTTP_404_NOT_FOUND)
        
        file_obj = shared_link.file
        shared_link.increment_download()

        internal_path = '/protected-media/' + file_obj.file.name.lstrip('/')  
        response = HttpResponse()
        response['Content-Type'] = file_obj.mime_type or 'application/octet-stream'
        response['Content-Disposition'] = f'attachment; filename="{file_obj.name}"'
        response['X-Accel-Redirect'] = internal_path
        return response