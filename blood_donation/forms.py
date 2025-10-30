from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import BloodDonor, BloodInventory, BloodRequest

# =====================
# User Registration Form
# =====================
class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")
        return cleaned_data


# =====================
# Staff Creation Form
# =====================
class StaffCreationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password"]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_staff = True   # force staff status
        if commit:
            user.save()
        return user


# =====================
# Blood Donor Form
# =====================
class BloodDonorForm(forms.ModelForm):
    class Meta:
        model = BloodDonor
        exclude = ['created_at']  # auto-filled, not editable
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'blood_type': forms.TextInput(attrs={'placeholder': 'Enter Blood Type'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'address1': forms.TextInput(attrs={'placeholder': 'Address Line 1'}),
            'address2': forms.TextInput(attrs={'placeholder': 'Address Line 2'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'region': forms.TextInput(attrs={'placeholder': 'State/Region'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'occupation': forms.TextInput(attrs={'placeholder': 'Occupation'}),
            'other_allergies': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Specify other allergies if any'}),
        }


# =====================
# Blood Inventory Form
# =====================
class BloodInventoryForm(forms.ModelForm):
    class Meta:
        model = BloodInventory
        fields = ['blood_type', 'quantity']
        widgets = {
            'blood_type': forms.TextInput(attrs={'placeholder': 'Enter Blood Type'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Enter Quantity'}),
        }


# =====================
# Blood Request Form
# =====================
# class BloodRequestForm(forms.ModelForm):
#     class Meta:
#         model = BloodRequest
#         fields = ['blood_type', 'quantity']
#         widgets = {
#             "blood_type": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Blood Type"}),
#             "quantity": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter Quantity"}),
#         }


class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['blood_type', 'units', 'status']  # ✅ Correct


from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['user', 'name', 'email', 'phone']  # staff fills these
