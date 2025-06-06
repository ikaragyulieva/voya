from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from django.utils.translation import gettext_lazy as _
from voya.requests.models import TripRequests


@admin.register(TripRequests)
class TripRequestsAdmin(SimpleHistoryAdmin):
    list_display = (
        'slug',
        'country_origin',
        'nationality',
        'trip_start_date',
        'trip_end_date',
        'budget',
        'is_active',
        'created_by_company',
    )

    list_filter = (
        'is_active',
        'country_origin',
        'nationality',
        'currency',
        'trip_start_date',
        'trip_end_date',
    )

    search_fields = ('slug', 'created_by_user__username', 'created_by_company__name')

    ordering = ('trip_start_date', 'budget')

    fieldsets = (
        (_("Trip Information"), {
            "fields": (
                'country_origin',
                'nationality',
                'country_destinations',
                'city_destinations',
                'other_destinations',
                'trip_start_date',
                'trip_end_date',
                'trip_duration',
                'budget',
                'currency',
            ),
        }),
        (_("Accommodations and Meals"), {
            "fields": (
                'accommodations',
                'accommodations_details',
                'meals',
                'meals_details',
            ),
        }),
        (_("Transportation"), {
            "fields": (
                'transportation_type',
                'transportation_details',
            ),
        }),
        (_("Group Details"), {
            "fields": (
                'age_range',
                'min_participants',
                'max_participants',
                'kind_of_group',
                'type_of_trip',
                'staff',
            ),
        }),
        (_("Administrative"), {
            "fields": (
                'is_active',
                'created_by_user',
                'created_by_company',
                'slug',
            ),
        }),
    )

    actions = ['mark_as_inactive', 'mark_as_active']

    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _("Selected requests were marked as inactive."))

    mark_as_inactive.short_description = _("Mark selected requests as inactive")

    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _("Selected requests were marked as active."))

    mark_as_active.short_description = _("Mark selected requests as active")

    readonly_fields = ('slug',)

    list_per_page = 10

    # Display latest historical record timestamp
    def history_latest(self, obj):
        latest_record = obj.history.first()
        return latest_record.history_date if latest_record else _("No history")

    history_latest.admin_order_field = 'history__history_date'
    history_latest.short_description = "Last Modified"
