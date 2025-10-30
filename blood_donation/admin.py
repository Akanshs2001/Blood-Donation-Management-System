from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile
from .models import BloodInventory



# Inline Profile with User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role',)

    def get_role(self, obj):
        return obj.profile.role
    get_role.short_description = 'Role'   # ✅ This changes the column name

# Unregister the original User admin, then register the new one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register Profile separately (optional)
admin.site.register(Profile)






from .models import Announcement, AvailableBlood, Campaign

# Register models in admin
admin.site.register(Announcement)
admin.site.register(AvailableBlood)
admin.site.register(Campaign)















from .models import Staff
from .forms import StaffCreationForm


class StaffAdmin(UserAdmin):
    add_form = StaffCreationForm
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("first_name", "last_name", "email", "username", "password", "confirm_password"),
        }),
    )
    list_display = ("username", "email", "first_name", "last_name", "is_staff")

    def get_queryset(self, request):
        """Show only staff users"""
        qs = super().get_queryset(request)
        return qs.filter(is_staff=True)


# ✅ Register Staff as a separate menu
admin.site.register(Staff, StaffAdmin)






from .models import BloodDonor


@admin.register(BloodDonor)
class BloodDonorAdmin(admin.ModelAdmin):
    list_display = (
        "first_name", "last_name", "email", "phone", "blood_type", "donated_before", "created_at"
    )
    list_filter = ("blood_type", "donated_before", "diseases", "allergies")  # ✅ removed positive_tests
    search_fields = ("first_name", "last_name", "email", "phone")

    fieldsets = (
        ("Donor Info", {
            "fields": ("first_name", "last_name", "date_of_birth", "email", "phone", "address", "occupation", "blood_type")
        }),
        ("Donation History", {
            "fields": ("donated_before",)
        }),
        ("Health Security Check", {
            "fields": ("diseases", "allergies", "other_allergies", "positive_tests", "cardiac_problems", "bleeding_disorders", "medication")
        }),
        ("System Info", {
            "fields": ("created_at",),
        }),
    )
    readonly_fields = ("created_at",)







from .models import BloodInventory

@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ("blood_type", "quantity", "last_updated")
    list_filter = ("blood_type",)
    search_fields = ("blood_type",)









from .models import BloodRequest

# @admin.register(BloodRequest)
# class BloodRequestAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'blood_type', 'quantity', 'status', 'requested_at', 'approved_at')
#     list_filter = ('blood_type', 'status')
#     search_fields = ('user__username', 'blood_type', 'status')




@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'blood_type', 'units', 'status')  # ✅ Correct
