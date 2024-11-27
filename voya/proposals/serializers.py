from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import transaction, models
from rest_framework import serializers

from voya.proposals.choices import SectionChoices
from voya.proposals.models import ProposalSectionItem, Proposal
# from voya.services import models
from voya.utils import get_user_obj


class DynamicServiceSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)

        if model:
            for field in model._meta.get_fields():
                if field.is_relation or field.name in ['id', 'created_at', 'updated_at']:
                    continue

                if isinstance(field, models.CharField):
                    self.fields[field.name] = serializers.CharField()
                elif isinstance(field, models.DecimalField):
                    self.fields[field.name] = serializers.DecimalField(max_digits=field.max_digits, decimal_places=field.decimal_places)
                elif isinstance(field, models.IntegerField):
                    self.fields[field.name] = serializers.IntegerField()
                elif isinstance(field, models.BooleanField):
                    self.fields[field.name] = serializers.BooleanField()


class ServiceListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    display_field = serializers.CharField()
    city = serializers.CharField()
    price = serializers.DecimalField(max_digits=5, decimal_places=2)


