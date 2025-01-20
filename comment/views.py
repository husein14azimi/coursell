# comment/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from .models import Comment
from .serializers import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter comments by content_type and object_id if provided
        content_type = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')
        if content_type and object_id:
            return Comment.objects.filter(content_type__model=content_type, object_id=object_id)
        return Comment.objects.none()

    def perform_create(self, serializer):
        # Ensure that the user is set correctly
        if not self.request.user.is_authenticated:
            raise ValidationError("User not authenticated")
        serializer.save(user=self.request.user)