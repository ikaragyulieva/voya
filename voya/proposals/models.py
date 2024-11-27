from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from voya.common.models import TimestampedModel
from voya.proposals.choices import SectionChoices

# Create your models here.

User = get_user_model()


class Proposal(TimestampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="proposals",
    )

    title = models.CharField(
        max_length=255,
    )

    is_draft = models.BooleanField(
        default=True,
    )


class ServiceLink(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    service = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('content_type', 'object_id')


class ProposalSectionItem(models.Model):
    proposal = models.ForeignKey(
        Proposal,
        on_delete=models.CASCADE,
        related_name='items',
    )

    section_name = models.CharField(
        max_length=50,
        choices=SectionChoices
    )

    quantity = models.PositiveIntegerField(default=1)

    additional_notes = models.TextField()

    corresponding_trip_date = models.DateField(
        blank=False,
        null=False,
    )

    services = models.ManyToManyField(
        ServiceLink,
        related_name='item_service'
    )

    @property
    def total_price(self):
        if self.services and hasattr(self.services, 'price'):
            return self.services.price * self.quantity
