from rest_framework import generics
from .models import File, User
from .serializers import FileSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FileUploadView(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return File.objects.all()
        elif user.role == 'editor':
            return File.objects.filter(uploaded_by=user)
        elif user.role == 'viewer':
            return File.objects.all()
        return File.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role in ['admin', 'editor']:
            # print(self.request.user.role)
            serializer.save(uploaded_by=self.request.user)
        else:
            raise PermissionError("You do not have permission to upload files.")

class FileDeleteView(generics.DestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        file = self.get_object()
        user = request.user
        if user.role == 'admin' or (user.role == 'editor' and file.uploaded_by == user):
            return super().delete(request, *args, **kwargs)
        return Response({"detail": "Permission denied"}, status=403)
