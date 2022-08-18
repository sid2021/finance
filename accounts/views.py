from decimal import Decimal
from django.http import Http404
from django.contrib.auth.models import User
from django.db import transaction

from rest_framework import generics
from rest_framework import mixins
from rest_framework import views
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .models import Transaction, Account
from .serializers import (
    AccountSerializer,
    TransactionSerializer,
    UserSerializer,
)
from .exceptions import InvalidBalance, InvalidAccount


class AccountListCreate(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView,
):
    """View responbsible for account creation and listing."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @swagger_auto_schema()
    def post(self, request: Request, *args, **kwargs) -> Response:
        """Create a new Account."""
        return self.create(request, *args, **kwargs)

    @swagger_auto_schema()
    def get(self, request: Request, *args, **kwargs) -> Response:
        """Get list of existing Accounts."""
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Override method to modify how the instance save is managed. We want
        the authenticated user from the incoming request to be associated
        with the newly created account.
        """
        serializer.save(owner=self.request.user)


class AccountDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """View responbsible for account retrieval."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @swagger_auto_schema()
    def get(self, request, *args, **kwargs):
        """Retrieve account data including balance and history."""
        return self.retrieve(request, *args, **kwargs)


class AccountHistory(views.APIView):
    """View responsible for listing account history."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """Get object instance or raise 404."""
        try:
            return Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            raise Http404

    @swagger_auto_schema()
    def get(self, request: Request, pk, format=None) -> Response:
        """Retrieve history of user's transactions for selected account."""
        account = self.get_object(pk)
        transactions = Transaction.objects.filter(account=account)
        serializer = TransactionSerializer(transactions, many=True)

        return Response(serializer.data)


class UserDetail(generics.RetrieveAPIView):
    """Retrieve selected User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class TransactionCreate(mixins.CreateModelMixin, generics.GenericAPIView):
    """View responbsible for new Transactions creation."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def validate_account(self):
        """Validate if Account exists and belongs to the authenticated user
        from the incoming request.
        """
        account = Account.objects.filter(
            pk=self.request.data.get("account", "")
        ).first()

        if not account:
            raise InvalidAccount("Account does not exist.")
        if account.owner != self.request.user:
            raise InvalidAccount(
                "Account does not belong to currently authenticated user."
            )

        self.account = account

    def validate_balance(self, type: str, amount: Decimal) -> None:
        """Validate if transaction if feasible. We do not allow negative
        balance.
        """
        if type == Transaction.TRANSFER:
            if self.account.balance - abs(amount) < 0:
                raise InvalidBalance("Not enough funds.")

    def update_balance(self, type: str, amount: Decimal) -> None:
        """Update Account balance."""
        if type == Transaction.DEPOSIT:
            self.account.balance += abs(amount)
        if type == Transaction.TRANSFER:
            self.account.balance -= abs(amount)
        self.account.save()

    @swagger_auto_schema()
    @transaction.atomic
    def post(self, request: Request, *args, **kwargs) -> Response:
        """Create a new Transaction."""
        type = request.data.get("type")
        amount = request.data.get("amount")
        self.validate_account()
        self.validate_balance(type=type, amount=Decimal(amount))
        self.update_balance(type=type, amount=Decimal(amount))
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer) -> None:
        """We want the created transaction to be associated with account id
        from the incoming request.
        """
        serializer.save(account=self.account)
