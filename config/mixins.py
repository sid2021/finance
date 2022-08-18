"""Core mixins for the application."""
import uuid

from django.db import models


class UUIDPrimaryKeyAbstractModel(models.Model):
    """An abstract class providing UUID as PK."""

    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """An abstract class providing self-updating created and modified
    fields.
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
