# comment/serializers.py

from rest_framework import serializers
from django_comments_xtd.models import XtdComment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = XtdComment
        fields = ['id', 'comment', 'user', 'submit_date', 'parent_id']  # Use 'parent_id' instead of 'parent'
        read_only_fields = ['id', 'submit_date', 'user']





# comment/serializers.py

from rest_framework import serializers
from django_comments_xtd.api.serializers import WriteCommentSerializer

class CustomWriteCommentSerializer(WriteCommentSerializer):
    def validate_name(self, value):
        # If the name is provided, use it
        if value.strip():
            return value.strip()
        
        # If the user is provided in the serializer.save() method, use their name
        user = self.context.get('user')
        if user and user.is_authenticated:
            return user.get_full_name() or user.get_username()
        
        # Otherwise, raise a validation error
        raise serializers.ValidationError("This field is required")

    def validate_email(self, value):
        # If the email is provided, use it
        if value.strip():
            return value.strip()
        
        # If the user is provided in the serializer.save() method, use their email
        user = self.context.get('user')
        if user and user.is_authenticated:
            return user.email
        
        # Otherwise, raise a validation error
        raise serializers.ValidationError("This field is required")