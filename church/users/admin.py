from django import forms
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from church.users.forms import UserAdminChangeForm, UserAdminCreationForm

from .models import Group, Member, Sermon

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


# @admin.register(Member)
# class MemberAdmin(admin.ModelAdmin):
# list_display = ("first_name", "last_name", "email", "phone_number")
# search_fields = ("first_name", "last_name", "email")


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "file":
            kwargs["widget"] = forms.ClearableFileInput(attrs={"multiple": False})
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    filter_horizontal = ("members",)


class MemberResource(resources.ModelResource):
    class Meta:
        model = Member


class MemberAdmin(ImportExportModelAdmin):
    resource_class = MemberResource
    list_display = ("first_name", "last_name", "email", "phone_number")
    search_fields = ("first_name", "last_name", "email")


# Re-register the Member model with the updated MemberAdmin class
#admin.site.unregister(Member)  # Unregister first to avoid duplicate registration
admin.site.register(Member, MemberAdmin)
