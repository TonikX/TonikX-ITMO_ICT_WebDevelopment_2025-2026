from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import (
    User, SecurityCompany, Category, Service,
    ServiceCategory, ServiceDiscount, ServiceRequest,
    Review, UserFavorite
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'surname', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('email', 'name', 'surname', 'patronymic')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('name', 'surname', 'patronymic')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'surname', 'patronymic', 'password1', 'password2'),
        }),
    )


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1
    readonly_fields = ('created_at', 'updated_at')
    fields = ('name', 'price', 'description', 'created_at', 'updated_at')


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('user', 'rating', 'comment', 'created_at')


@admin.register(SecurityCompany)
class SecurityCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'average_rating_display', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'average_rating_display')
    inlines = [ServiceInline, ReviewInline]

    def average_rating_display(self, obj):
        """Отображение среднего рейтинга с цветом"""
        rating = obj.average_rating
        if rating is None:
            rating = 0

        if rating >= 4:
            color = 'green'
        elif rating >= 3:
            color = 'orange'
        else:
            color = 'red'

        rating_formatted = f"{rating:.1f}"

        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            rating_formatted
        )

    average_rating_display.short_description = 'Средний рейтинг'


class ServiceDiscountInline(admin.TabularInline):
    model = ServiceDiscount
    extra = 1
    readonly_fields = ('created_at', 'updated_at')
    fields = ('discount_percent', 'start_date', 'end_date', 'created_at', 'updated_at')


class ServiceCategoryInline(admin.TabularInline):
    model = ServiceCategory
    extra = 1
    autocomplete_fields = ['category']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'security_company', 'price', 'current_price_display', 'created_at')
    list_filter = ('security_company', 'created_at')
    search_fields = ('name', 'description', 'security_company__name')
    readonly_fields = ('created_at', 'updated_at', 'current_price_display')
    inlines = [ServiceCategoryInline, ServiceDiscountInline]
    fields = ('security_company', 'name', 'description', 'price')

    def current_price_display(self, obj):
        """Отображение текущей цены со скидкой"""
        current_price = obj.current_price
        if current_price < obj.price:
            return format_html(
                '<span style="color: red; text-decoration: line-through;">{}</span> <strong>{}</strong>',
                obj.price,
                current_price
            )
        return obj.price

    current_price_display.short_description = 'Текущая цена'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'services_count')
    search_fields = ('name',)

    def services_count(self, obj):
        return obj.services.count()

    services_count.short_description = 'Количество услуг'


@admin.register(ServiceDiscount)
class ServiceDiscountAdmin(admin.ModelAdmin):
    list_display = ('service', 'discount_percent', 'start_date', 'end_date', 'is_active_display', 'created_at')
    list_filter = ('start_date', 'end_date', 'created_at')
    search_fields = ('service__name', 'service__security_company__name')
    readonly_fields = ('created_at', 'updated_at', 'is_active_display')

    def is_active_display(self, obj):
        """Отображение активности скидки"""
        is_active = obj.is_active()
        if is_active:
            return format_html(
                '<span style="color: green; font-weight: bold;">Активна</span>'
            )
        return format_html(
            '<span style="color: gray;">Не активна</span>'
        )

    is_active_display.short_description = 'Статус'


class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'status', 'colored_status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('user__email', 'service__name', 'description', 'admin_comment')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)

    def colored_status(self, obj):
        """Цветовая индикация статуса"""
        colors = {
            'pending': 'orange',
            'confirmed': 'green',
            'in_progress': 'blue',
            'completed': 'gray',
            'cancelled': 'red',
        }
        status_display = dict(obj.STATUS_CHOICES).get(obj.status, obj.status)
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            status_display
        )

    colored_status.short_description = 'Цвет статуса'
    colored_status.admin_order_field = 'status'


admin.site.register(ServiceRequest, ServiceRequestAdmin)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'security_company', 'rating_display', 'created_at')
    list_filter = ('rating', 'created_at', 'security_company')
    search_fields = ('user__email', 'security_company__name', 'comment')
    readonly_fields = ('created_at',)

    def rating_display(self, obj):
        """Отображение рейтинга звездами"""
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html(
            '<span style="color: gold; font-size: 16px;">{}</span> ({})',
            stars,
            obj.rating
        )

    rating_display.short_description = 'Рейтинг'


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'service__name')
    readonly_fields = ('created_at',)


admin.site.register(ServiceCategory)