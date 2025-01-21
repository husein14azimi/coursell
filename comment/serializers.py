# comment/serializers.py
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from jalali.serializers import JalaliDateTimeField


class CommentSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(write_only=True)  # Accept content_type as a string
    object_pk = serializers.IntegerField(write_only=True)
    created_at = JalaliDateTimeField(required=False, allow_null=True)
    updated_at = JalaliDateTimeField(required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = ['id', 'content_type', 'object_pk', 'text', 'user', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Extract content_type and object_pk
        content_type = validated_data.pop('content_type')
        object_pk = validated_data.pop('object_pk')  # Renamed from object_id to object_pk

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
            object_pk=object_pk,  # Updated to object_pk
            **validated_data
        )
        return comment