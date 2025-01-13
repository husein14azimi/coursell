# account.serializers

from django.contrib.auth import get_user_model
from rest_framework import serializers

User  = get_user_model()

class CombinedUserPersonSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source='person.bio', allow_blank=True, required=False)
    birth_date = serializers.DateField(source='person.birth_date', allow_null=True, required=False)
    gender = serializers.CharField(source='person.gender', allow_null=True, required=False)

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'password', 'bio', 'birth_date', 'gender']
        read_only_fields = ['id', 'username']