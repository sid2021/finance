from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from config.mixins import TimeStampedModel


class Account(TimeStampedModel):
    """Model storing information on user's bank account."""

    USD = "USD"
    EUR = "EUR"
    CURRENCY_CHOICES = [(USD, "USD"), (EUR, "EUR")]

    owner = models.ForeignKey(
        User, related_name="accounts", on_delete=models.CASCADE
    )
    balance = models.DecimalField(
        decimal_places=2, default=Decimal(0), max_digits=12
    )
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, help_text="Type of currency."
    )

    def __str__(self):
        return f"Account {self.pk} | {self.owner} | {self.currency}"

    def change_balance(self, amount: Decimal) -> None:
        """Make a deposit."""
        self.balance += amount


class Transaction(TimeStampedModel):
    """Model storing information of a given transaction."""

    DEPOSIT = "Deposit"
    TRANSFER = "Transfer"
    TRANSACTION_CHOICES = [
        (DEPOSIT, "Deposit"),
        (TRANSFER, "Transfer"),
    ]

    account = models.ForeignKey(
        Account, related_name="transactions", on_delete=models.CASCADE
    )
    type = models.CharField(
        max_length=8,
        choices=TRANSACTION_CHOICES,
        help_text="Type of transaction",
    )
    amount = models.DecimalField(
        decimal_places=2, default=Decimal(0), max_digits=12
    )

    def __str__(self):
        return (
            f"Transaction {self.type} for {self.amount} {self.account.currency}"
        )
