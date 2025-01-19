# comment/views.py

from rest_framework import viewsets, permissions
from django.contrib.contenttypes.models import ContentType
from django_comments_xtd.models import XtdComment
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import CommentSerializer, CustomWriteCommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer  # Use CommentSerializer for read operations
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = XtdComment.objects.all()

    def get_serializer_class(self):
        # Use CustomWriteCommentSerializer for write operations (create, update, etc.)
        if self.action in ['create', 'update', 'partial_update', 'reply']:
            return CustomWriteCommentSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        # Get the content type and object ID from the request data
        content_type = serializer.validated_data['content_type']
        object_pk = serializer.validated_data['object_pk']
        # Pass the user to the serializer context
        serializer.save(user=self.request.user, content_type=content_type, object_pk=object_pk)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reply(self, request, pk=None):
        parent_comment = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Pass the user to the serializer context
        serializer.save(
            user=request.user,
            parent_id=parent_comment.id,
            content_type=parent_comment.content_type,
            object_pk=parent_comment.object_pk
        )
        return Response(serializer.data, status=201)