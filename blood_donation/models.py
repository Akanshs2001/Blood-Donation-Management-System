from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone  # for default timestamps

# =====================
# Profile Model
# =====================
class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('user', 'User'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# 🔔 Signals to auto-create or update Profile
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)


# =====================
# Announcements
# =====================
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# =====================
# Available Blood
# =====================
class AvailableBlood(models.Model):
    BLOOD_GROUPS = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-"),
    ]
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    units = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.blood_group} - {self.units} units"


# =====================
# Campaigns
# =====================
class Campaign(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# =====================
# Staff Proxy
# =====================
class Staff(User):
    class Meta:
        proxy = True
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"


# =====================
# Donors
# =====================
class BloodDonor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    blood_type = models.CharField(max_length=5)

    donated_before = models.CharField(max_length=3, choices=[("Yes", "Yes"), ("No", "No")])
    diseases = models.CharField(max_length=3, choices=[("Yes", "Yes"), ("No", "No")])
    allergies = models.CharField(max_length=3, choices=[("Yes", "Yes"), ("No", "No")])
    other_allergies = models.TextField(blank=True, null=True)
    positive_test = models.CharField(max_length=3, choices=[("Yes", "Yes"), ("No", "No")])
    cardiac = models.CharField(max_length=3, choices=[("Yes", "Yes"), ("No", "No")])
    bleeding = models.CharField(max_length=3, choices=[("Yes", "Yes"), ("No", "No")])
    medication = models.CharField(max_length=3, choices=[("Yes", "Yes"), ("No", "No")])

    eligibility = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.blood_type}"


# =====================
# Blood Inventory
# =====================
class BloodInventory(models.Model):
    blood_type = models.CharField(max_length=5, unique=True)
    quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.blood_type} - {self.quantity} units"


# =====================
# Blood Requests
# =====================
class BloodRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=5)
    units = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")],
        default="Pending"
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.blood_type} ({self.units})"


# =====================
# Donations
# =====================
class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='marked_donations')
    name = models.CharField(max_length=100, default="Anonymous")  # default for existing rows
    email = models.EmailField(null=True, blank=True, default="test@example.com")  # default for existing rows
    phone = models.CharField(max_length=15, default="0000000000")  # default for existing rows
    date = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"


# =====================
# Optional Notification Model
# =====================
# class Notification(models.Model):
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)
#     role = models.CharField(
#         max_length=10,
#         choices=[("admin", "Admin"), ("staff", "Staff")],
#         default="staff"
#     )

#     def __str__(self):
#         return self.message
