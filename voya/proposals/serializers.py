
from rest_framework import serializers

from voya.proposals.choices import SectionChoices
from voya.requests import choices


class ProposalSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=255,
        error_messages={
            'blank': 'The proposal title is required.',
            'max_length': 'The title must not exceed 255 characters.',
        }
    )

    is_draft = serializers.BooleanField(default=True)


class ItemSerializer(serializers.Serializer):
    section_name = serializers.ChoiceField(
        choices=SectionChoices,
        error_messages={
            'invalid_choice': 'Invalid section name. Please select a valid section.',
        }
    )

    service_id = serializers.IntegerField()
    quantity = serializers.IntegerField(
        min_value=1,
        error_messages={
            'min_value': 'Quantity must be at least 1.',
            'invalid': 'Quantity must be a number.',
        }
    )
    additional_notes = serializers.CharField(allow_blank=True)
    corresponding_trip_date = serializers.DateField(
        error_messages={
            'invalid': 'Invalid date format. Please use YYYY-MM-DD.',
            'null': 'Trip date is required.',
        }
    )
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    city = serializers.ChoiceField(
        choices=choices.CityChoices,
        error_messages={
            'invalid_choice': 'Invalid city. Please select a valid city.',
        }
    )


class BudgetSerializer(serializers.Serializer):
    pax = serializers.IntegerField()
    variable_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    fixed_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_cost_per_person = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    service_fee = serializers.DecimalField(max_digits=10, decimal_places=2)
    margin = serializers.IntegerField()
    fina_price_per_person = serializers.DecimalField(max_digits=10, decimal_places=2)
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2)
