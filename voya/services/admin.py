from django.contrib import admin

from voya.services.models import Hotel, Transfer, LocalGuide, Ticket, Currency, PublicTransport, PrivateTransport


@admin.register(Hotel)
class HotelsAdmin(admin.ModelAdmin):
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
        ('Hotel Information', {
            'fields': (
                'name',
                'category',
                'high_season_price',
                'low_season_price'
            )
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected hotels have been marked as active.")
    mark_active.short_description = "Mark selected hotels as active"

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected hotels have been marked as inactive.")
    mark_inactive.short_description = "Mark selected hotels as inactive"


@admin.register(Transfer)
class TransfersAdmin(admin.ModelAdmin):
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
        ('Transfer Information', {
            'fields': ('transfer_name', 'type', 'price')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected transfers have been marked as active.")
    mark_active.short_description = "Mark selected transfers as active"

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected transfers have been marked as inactive.")
    mark_inactive.short_description = "Mark selected transfers as inactive"


@admin.register(LocalGuide)
class LocalGuidesAdmin(admin.ModelAdmin):
    list_display = (
        'guide_name',
        'price',
        'tour_duration',
        'is_active',
        'updated_at',
    )

    search_fields = ('guide_name', 'price_includes')

    list_filter = ('is_active',)

    ordering = ('guide_name',)

    fieldsets = (
        ('Guide Information', {
            'fields': ('guide_name', 'price', 'price_includes', 'tour_duration')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected guides have been marked as active.")
    mark_active.short_description = "Mark selected guides as active"

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected guides have been marked as inactive.")
    mark_inactive.short_description = "Mark selected guides as inactive"


@admin.register(Ticket)
class TicketsAdmin(admin.ModelAdmin):
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
        ('Ticket Information', {
            'fields': ('name', 'price', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected tickets have been marked as active.")
    mark_active.short_description = "Mark selected tickets as active"

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected tickets have been marked as inactive.")
    mark_inactive.short_description = "Mark selected tickets as inactive"


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
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
        ('Currency Information', {
            'fields': ('currency_from', 'currency_to', 'exchange_rate')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Created By', {
            'fields': ('created_by_user',)
        }),
    )


@admin.register(PublicTransport)
class PublicTransportAdmin(admin.ModelAdmin):
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
        ('Transport Information', {
            'fields': ('type', 'price')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected public transport options have been marked as active.")
    mark_active.short_description = "Mark selected public transport as active"

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected public transport options have been marked as inactive.")
    mark_inactive.short_description = "Mark selected public transport as inactive"


@admin.register(PrivateTransport)
class PrivateTransportAdmin(admin.ModelAdmin):
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
        ('Transport Information', {
            'fields': ('type', 'price')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected private transport options have been marked as active.")
    mark_active.short_description = "Mark selected private transport as active"

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected private transport options have been marked as inactive.")
    mark_inactive.short_description = "Mark selected private transport as inactive"
