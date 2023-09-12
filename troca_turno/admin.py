from django.contrib import admin
from troca_turno.models import Operacao, MobyUser, Torre, Passagem

from django.contrib.auth.admin import UserAdmin
from troca_turno.models import MobyUser
from troca_turno.forms import MobyUserCreationForm, MobyUserChangeForm

admin.site.register(Operacao)
admin.site.register(Torre)
admin.site.register(Passagem)

class CustomUserAdmin(UserAdmin):
    add_form = MobyUserCreationForm
    form = MobyUserChangeForm
    model = MobyUser
    list_display = ('email', 'operacao')
    list_filter = ('email', 'operacao')

    fieldsets = (
        (None, {"fields": ("email", "username", "password", "operacao", "gestor")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "username","password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions", "operacao", "gestor"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(MobyUser, CustomUserAdmin)
