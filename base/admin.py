from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Client, EnvironmentalMetric, Recommendation, DataSource, Alert, ActionItem, HistoricalData

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('username', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email',)
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Client)
admin.site.register(EnvironmentalMetric)
admin.site.register(Recommendation)
admin.site.register(DataSource)
admin.site.register(Alert)
admin.site.register(ActionItem)
admin.site.register(HistoricalData)
