from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from django.utils.translation import gettext_lazy as _
from voya.services.models import Hotel, Transfer, LocalGuide, Ticket, Currency, PublicTransport, PrivateTransport, \
    Location


@admin.register(Hotel)
class HotelsAdmin(SimpleHistoryAdmin):
    list_display = (
        'name',
        'category',
        'high_season_price',
        'low_season_price',
        'is_active',
        'updated_at',
    )

    search_fields = (
        'name',
        'category'
    )

    list_filter = ('category', 'is_active')

    ordering = ('name',)

    fieldsets = (
        (_('Hotel Information'), {
            'fields': (
                'name',
                'category',
                'high_season_price',
                'low_season_price'
            )
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )

    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _("Selected hotels have been marked as active."))
    mark_active.short_description = _("Mark selected hotels as active")

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _("Selected hotels have been marked as inactive."))
    mark_inactive.short_description = _("Mark selected hotels as inactive")

    # Display latest historical record timestamp
    def history_latest(self, obj):
        latest_record = obj.history.first()
        return latest_record.history_date if latest_record else _("No history")

    history_latest.admin_order_field = 'history__history_date'
    history_latest.short_description = _("Last Modified")


@admin.register(Transfer)
class TransfersAdmin(SimpleHistoryAdmin):
    list_display = (
        'transfer_name',
        'type',
        'price',
        'is_active',
        'updated_at',
    )

    search_fields = ('transfer_name', 'type')

    list_filter = ('type', 'is_active')

    ordering = ('transfer_name',)

    fieldsets = (
        (_('Transfer Information'), {
            'fields': ('transfer_name', 'type', 'price')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )

    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _("Selected transfers have been marked as active."))
    mark_active.short_description = _("Mark selected transfers as active")

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _("Selected transfers have been marked as inactive."))
    mark_inactive.short_description = _("Mark selected transfers as inactive")

    # Display latest historical record timestamp
    def history_latest(self, obj):
        latest_record = obj.history.first()
        return latest_record.history_date if latest_record else _("No history")

    history_latest.admin_order_field = 'history__history_date'
    history_latest.short_description = _("Last Modified")


@admin.register(LocalGuide)
class LocalGuidesAdmin(SimpleHistoryAdmin):
    list_display = (
        'name',
        'price',
        'tour_description',
        'is_active',
        'updated_at',
    )

    search_fields = ('name', 'price_includes')

    list_filter = ('is_active',)

    ordering = ('name',)

    fieldsets = (
        (_('Guide Information'), {
            'fields': ('name', 'price', 'price_includes', 'tour_duration')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )

    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _("Selected guides have been marked as active."))
    mark_active.short_description = _("Mark selected guides as active")

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _("Selected guides have been marked as inactive."))
    mark_inactive.short_description = _("Mark selected guides as inactive")

    # Display latest historical record timestamp
    def history_latest(self, obj):
        latest_record = obj.history.first()
        return latest_record.history_date if latest_record else _("No history")

    history_latest.admin_order_field = 'history__history_date'
    history_latest.short_description = _("Last Modified")


@admin.register(Ticket)
class TicketsAdmin(SimpleHistoryAdmin):
    list_display = (
        'name',
        'price',
        'city',
        'is_active',
        'updated_at',
    )

    search_fields = ('name', 'description')

    list_filter = ('is_active', 'city', 'name')

    ordering = ('name',)

    fieldsets = (
        (_('Ticket Information'), {
            'fields': ('name', 'price', 'description')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )

    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _("Selected tickets have been marked as active."))
    mark_active.short_description = _("Mark selected tickets as active")

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _("Selected tickets have been marked as inactive."))
    mark_inactive.short_description = _("Mark selected tickets as inactive")

    # Display latest historical record timestamp
    def history_latest(self, obj):
        latest_record = obj.history.first()
        return latest_record.history_date if latest_record else _("No history")

    history_latest.admin_order_field = 'history__history_date'
    history_latest.short_description = _("Last Modified")


@admin.register(Currency)
class CurrencyAdmin(SimpleHistoryAdmin):
    list_display = (
        'currency_from',
        'currency_to',
        'exchange_rate',
        'is_active',
        'updated_at',
    )

    search_fields = ('currency_from', 'currency_to', 'created_by_user__email')

    list_filter = ('is_active', 'currency_from', 'currency_to')

    ordering = ('currency_from', 'currency_to')

    fieldsets = (
        (_('Currency Information'), {
            'fields': ('currency_from', 'currency_to', 'exchange_rate')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
        (_('Created By'), {
            'fields': ('created_by_user',)
        }),
    )

    # Display latest historical record timestamp
    def history_latest(self, obj):
        latest_record = obj.history.first()
        return latest_record.history_date if latest_record else _("No history")

    history_latest.admin_order_field = 'history__history_date'
    history_latest.short_description = _("Last Modified")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'city_name',
        'country',
    )

    search_fields = ('city_name', 'country')

    list_filter = ('city_name', 'country')

    ordering = ('country', 'city_name')

    fieldsets = (
        (_('Location Information'), {
            'fields': ('city_name', 'country')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
        (_('Created By'), {
            'fields': ('created_by_user',)
        }),
    )


@admin.register(PublicTransport)
class PublicTransportAdmin(SimpleHistoryAdmin):
    list_display = (
        'type',
        'price',
        'is_active',
        'updated_at',
    )

    search_fields = ('type',)

    list_filter = ('type', 'is_active')

    ordering = ('type',)

    fieldsets = (
        (_('Transport Information'), {
            'fields': ('type', 'price')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )

    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _("Selected public transport options have been marked as active."))
    mark_active.short_description = _("Mark selected public transport as active")

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _("Selected public transport options have been marked as inactive."))
    mark_inactive.short_description = _("Mark selected public transport as inactive")

    # Display latest historical record timestamp
    def history_latest(self, obj):
        latest_record = obj.history.first()
        return latest_record.history_date if latest_record else _("No history")

    history_latest.admin_order_field = 'history__history_date'
    history_latest.short_description = _("Last Modified")


@admin.register(PrivateTransport)
class PrivateTransportAdmin(SimpleHistoryAdmin):
    list_display = (
        'type',
        'price',
        'is_active',
        'updated_at',
    )

    search_fields = ('type',)

    list_filter = ('type', 'is_active')

    ordering = ('type',)

    fieldsets = (
        (_('Transport Information'), {
            'fields': ('type', 'price')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )

    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _("Selected private transport options have been marked as active."))
    mark_active.short_description = _("Mark selected private transport as active")

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _("Selected private transport options have been marked as inactive."))
    mark_inactive.short_description = _("Mark selected private transport as inactive")

    # Display latest historical record timestamp
    def history_latest(self, obj):
        latest_record = obj.history.first()
        return latest_record.history_date if latest_record else _("No history")

    history_latest.admin_order_field = 'history__history_date'
    history_latest.short_description = _("Last Modified")
