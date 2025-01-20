# comment/serializers.py
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(write_only=True)  # Accept content_type as a string
    object_id = serializers.IntegerField(write_only=True)  # Accept object_id as an integer

    class Meta:
        model = Comment
        fields = ['id', 'content_type', 'object_id', 'text', 'user', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Extract content_type and object_id
        content_type = validated_data.pop('content_type')
        object_id = validated_data.pop('object_id')

        # Get the ContentType instance
        try:
            content_type = ContentType.objects.get(model=content_type)
        except ContentType.DoesNotExist:
            raise serializers.ValidationError("Invalid content_type")

        # Automatically set the user to the currently logged-in user
        validated_data['user'] = self.context['request'].user

        # Create the comment
        comment = Comment.objects.create(
            content_type=content_type,
            object_id=object_id,
            **validated_data
        )
        return comment