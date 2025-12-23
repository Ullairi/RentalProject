from rest_framework import serializers
from .models import User, Favorite
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    """User serializer for registration"""
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'},
    )
    password_confirmation = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type':'password'}
    )
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'password_confirmation',
            'first_name', 'last_name', 'role', 'gender', 'birth_date',
            'phone', 'age', 'created_at'
        ]
        read_only_fields = ['id', 'age', 'created_at']

    def validate(self, val):
        """Check that passwords match"""
        if val.get('password') != val.get('password_confirmation'):
            raise serializers.ValidationError({
                'password_confirmation': 'Passwords dont match'
            })
        return val

    def create(self, validated_data):
        """Creation of a user with hashed password"""
        validated_data.pop('password_confirmation')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile shown"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    age = serializers.IntegerField(read_only=True)
    is_owner = serializers.BooleanField(read_only=True)
    is_tenant = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'role', 'gender', 'birth_date', 'age',
            'phone', 'is_owner', 'is_tenant', 'created_at'
        ]
        read_only_fields = fields


class UserInfoUpdateSerializer(serializers.ModelSerializer):
    """Serializer for user info update"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'birth_date', 'phone']


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for wish list management"""
    user = UserProfileSerializer(read_only=True)
    listing_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'listing', 'listing_id', 'created_at']
        read_only_fields = ['id', 'user', 'listing', 'created_at']