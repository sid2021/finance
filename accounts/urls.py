from django.urls import path
from .views import (
    AccountHistory,
    AccountListCreate,
    AccountDetail,
    UserDetail,
    TransactionCreate,
)

urlpatterns = [
    path("account/", AccountListCreate.as_view()),
    path("account/history/<int:pk>/", AccountHistory.as_view()),
    path("account/balance/<int:pk>/", AccountDetail.as_view()),
    path("users/<int:pk>/", UserDetail.as_view()),
    path("transaction/", TransactionCreate.as_view(), name="transaction"),
]
