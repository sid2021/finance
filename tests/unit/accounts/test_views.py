from decimal import Decimal
import pytest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from accounts.models import Account


@pytest.fixture
def api_client() -> APIClient:
    """Return an authorized APIClient object."""
    test_user = get_user_model().objects.create_user(
        username="foo", password="bar"
    )
    token = Token.objects.create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client


@pytest.mark.django_db()
def test_transaction_endpoint_returns_200(
    api_client: APIClient,
) -> None:
    """Test that the transaction endpoint returns 200 status when
    authentication and validation was succefull. Test that balance
    after transaction is correct.
    """
    url = reverse("transaction")
    payload = {
        "type": "Transfer",
        "account": "1",
        "amount": "-500",
    }
    user = get_user_model().objects.all().first()
    account = Account.objects.create(
        owner=user, currency=Account.USD, balance=Decimal(1000)
    )
    response = api_client.post(url, data=payload)
    account.refresh_from_db()
    assert response.status_code == status.HTTP_201_CREATED
    assert account.balance == Decimal(500)


@pytest.mark.django_db()
def test_transaction_endpoint_returns_400_with_not_sufficient_funds(
    api_client: APIClient,
) -> None:
    """Test that the transaction endpoint returns 400 status when
    there are not enough funds on account to perform transaction.
    """
    url = reverse("transaction")
    payload = {
        "type": "Transfer",
        "account": "2",
        "amount": "1000000",
    }
    user = get_user_model().objects.all().first()
    Account.objects.create(
        owner=user, currency=Account.USD, balance=Decimal(1000)
    )
    response = api_client.post(url, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == ["Not enough funds."]


@pytest.mark.django_db
def test_transaction_endpoint_returns_400_for_unauthenticated_user(
    api_client: APIClient,
) -> None:
    """Test that the transaction endpoint returns 400 status for
    user trying to create transaction using an account that does
    not belong to him.
    """
    url = reverse("transaction")
    payload = {
        "type": "Deposit",
        "account": "1",
        "amount": "20",
    }
    response = api_client.post(url, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == ["Account does not exist."]
