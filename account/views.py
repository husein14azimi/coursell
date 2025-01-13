# account.views

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from .serializers import CombinedUserPersonSerializer
from .models import Person
from django.contrib.auth import get_user_model

User  = get_user_model()

class CombinedUserProfileViewSet(viewsets.GenericViewSet):
    serializer_class = CombinedUserPersonSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny()]  # Open to all users
        return [IsAuthenticated()]  # Other actions require authentication

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract user data
        user_data = {
            'email': serializer.validated_data['email'],
            'phone_number': serializer.validated_data['phone_number'],
            'password': serializer.validated_data['password'],
        }

        # Create the user
        user = User.objects.create_user(**user_data)

        # Create the person instance if provided
        person_data = {
            'bio': serializer.validated_data.get('bio', ''),
            'birth_date': serializer.validated_data.get('birth_date', None),
            'gender': serializer.validated_data.get('gender', None),
        }
        Person.objects.create(user=user, **person_data)

        return Response(serializer.data, status=201)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Update user fields
        user.email = serializer.validated_data.get('email', user.email)
        user.phone_number = serializer.validated_data.get('phone_number', user.phone_number)
        if 'password' in serializer.validated_data:
            user.set_password(serializer.validated_data['password'])
        user.save()

        # Update person instance if it exists
        person_data = {
            'bio': serializer.validated_data.get('bio', ''),
            'birth_date': serializer.validated_data.get('birth_date', None),
            'gender': serializer.validated_data.get('gender', None),
        }
        person = user.person
        for attr, value in person_data.items():
            setattr(person, attr, value)
        person.save()

        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)