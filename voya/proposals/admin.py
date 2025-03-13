"""
Copyright (C) 2025 DROMO SA

This file is part of VOYA.

VOYA is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

[Project Name] is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from voya.proposals.models import ProposalBudget, ProposalSectionItem, Proposal


@admin.register(Proposal)
class ProposalAdmin(SimpleHistoryAdmin):
    """Admin configuration for Proposal."""
    list_display = (
        'title',
        'trip_request',
        'status',
        'created_at',
        'user',
    )

    search_fields = (
        'title',
        'user__email',
        'trip_request__slug',
    )

    list_filter = (
        'status',
        'created_at',
    )

    ordering = ('-created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title',
                'user',
                'trip_request',
                'status',
            )
        }),
    )

    # actions = ['mark_as_draft', 'mark_as_published']
    #
    # def mark_as_draft(self, request, queryset):
    #     queryset.update(is_draft=True)
    #     self.message_user(request, "Selected proposals have been marked as draft.")
    #
    # mark_as_draft.short_description = "Mark selected proposals as draft"
    #
    # def mark_as_published(self, request, queryset):
    #     queryset.update(is_draft=False)
    #     self.message_user(request, "Selected proposals have been marked as published.")
    #
    # mark_as_published.short_description = "Mark selected proposals as published"

    list_per_page = 10

    # Display latest historical record timestamp
    def history_latest(self, obj):
        latest_record = obj.history.first()
        return latest_record.history_date if latest_record else "No history"

    history_latest.admin_order_field = 'history__history_date'
    history_latest.short_description = "Last Modified"


@admin.register(ProposalSectionItem)
class ProposalSectionItemAdmin(SimpleHistoryAdmin):
    """Admin configuration for ProposalSectionItem."""
    list_display = (
        'proposal',
        'section_name',
        'city',
        'price',
    )

    search_fields = (
        'proposal__title',
        'section_name',
        'city',
    )

    list_filter = (
        'section_name',
        'city',
    )
    ordering = ('proposal', 'section_name', 'corresponding_trip_date')

    fieldsets = (
        ('Section Item Details', {
            'fields': (
                'proposal',
                'section_name',
                'service_id',
                'quantity',
                'corresponding_trip_date',
                'city',
                'price',
                'additional_notes',
            )
        }),
    )

    # Display latest historical record timestamp
    def history_latest(self, obj):
        latest_record = obj.history.first()
        return latest_record.history_date if latest_record else "No history"

    history_latest.admin_order_field = 'history__history_date'
    history_latest.short_description = "Last Modified"


@admin.register(ProposalBudget)
class ProposalBudgetAdmin(SimpleHistoryAdmin):
    """Admin configuration for ProposalBudget."""
    list_display = (
        'proposal',
        'pax',
        'total_cost',
        'final_price',
    )

    search_fields = (
        'proposal__title',
    )

    list_filter = (
        'margin',
        'service_fee',
    )

    ordering = ('proposal', 'pax')

    fieldsets = (
        ('Budget Details', {
            'fields': (
                'proposal',
                'pax',
                'variable_cost',
                'fixed_cost',
                'free_of_charge',
                'free_of_charge_amount',
                'total_cost_per_person',
                'total_cost',
                'service_fee',
                'margin',
                'fina_price_per_person',
                'final_price',
            )
        }),
    )

    # Display latest historical record timestamp
    def history_latest(self, obj):
        latest_record = obj.history.first()
        return latest_record.history_date if latest_record else "No history"

    history_latest.admin_order_field = 'history__history_date'
    history_latest.short_description = "Last Modified"
