from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Account, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model."""

    class Meta:
        model = Transaction
        fields = ["id", "created", "type", "amount", "account"]


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for the Account model."""

    owner = serializers.ReadOnlyField(source="owner.username")
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ["id", "balance", "currency", "owner", "transactions"]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    accounts = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Account.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "accounts"]
