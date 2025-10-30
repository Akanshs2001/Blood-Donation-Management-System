from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Donation
from .forms import DonationForm
from .forms import BloodDonorForm, BloodInventoryForm, BloodRequestForm
from .models import (
    BloodDonor, Campaign, Announcement, AvailableBlood,
    BloodInventory, BloodRequest
)

# ----------------- Home -----------------
def home(request):
    return render(request, 'home.html')


# ----------------- Login -----------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")

            if user.is_superuser:
                return redirect("/admin/")
            elif user.is_staff:
                return redirect("staff_dashboard")
            else:
                return redirect("user_dashboard")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "login.html")


# ----------------- Register -----------------
def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("register")

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password
        )
        user.is_staff = False
        user.save()

        messages.success(request, "Registration successful! You can now login.")
        return redirect("login")

    return render(request, "register.html")


# ----------------- Logout -----------------
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")


# ----------------- Dashboards -----------------
def user_dashboard(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return render(request, "user_dashboard.html")
    else:
        messages.error(request, "Access denied!")
        return redirect("login")


def staff_dashboard(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, "staff_dashboard.html")
    else:
        messages.error(request, "Access denied!")
        return redirect("login")


# ----------------- Donor Form -----------------
def donate_blood(request):
    if request.method == "POST":
        form = BloodDonorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Thank you! Your donation form has been submitted.")
            return redirect('donate_blood')
    else:
        form = BloodDonorForm()
    return render(request, 'donate_blood.html', {'form': form})


# ----------------- Donor List -----------------
@login_required
def donor_list(request):
    donors = BloodDonor.objects.all().order_by('-created_at')
    return render(request, 'donor_list.html', {'donors': donors})


# ----------------- Extra User Pages -----------------
def available_blood(request):
    stocks = AvailableBlood.objects.all()
    return render(request, "available_blood.html", {"stocks": stocks})


def campaigns(request):
    campaigns_list = Campaign.objects.all().order_by("date")
    return render(request, "campaigns.html", {"campaigns": campaigns_list})


def announcements(request):
    announcements_list = Announcement.objects.all().order_by("-created_at")
    return render(request, "announcements.html", {"announcements": announcements_list})


# ----------------- Staff: Manage Users -----------------
@login_required
def manage_users(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect("login")

    users = User.objects.all().order_by("id")
    return render(request, "manage_users.html", {"users": users})


# ----------------- Staff: Blood Inventory -----------------
@login_required
def staff_blood_inventory(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect("login")

    inventory = BloodInventory.objects.all().order_by("blood_type")
    return render(request, "staff_blood_inventory.html", {"inventory": inventory})


@login_required
def add_blood_inventory(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect("login")

    if request.method == "POST":
        form = BloodInventoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Blood inventory added successfully.")
            return redirect("staff_blood_inventory")
    else:
        form = BloodInventoryForm()

    return render(request, "blood_inventory_form.html", {"form": form, "title": "Add Blood Inventory"})


@login_required
def edit_blood_inventory(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect("login")

    inventory_item = get_object_or_404(BloodInventory, pk=pk)
    if request.method == "POST":
        form = BloodInventoryForm(request.POST, instance=inventory_item)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Blood inventory updated successfully.")
            return redirect("staff_blood_inventory")
    else:
        form = BloodInventoryForm(instance=inventory_item)

    return render(request, "blood_inventory_form.html", {"form": form, "title": "Edit Blood Inventory"})


# ----------------- User: Blood Request -----------------
@login_required
def request_blood(request):
    if request.method == "POST":
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.user = request.user
            blood_request.save()
            messages.success(request, "Your blood request has been submitted successfully!")
            return redirect('request_blood')
    else:
        form = BloodRequestForm()

    return render(request, "request_blood.html", {"form": form})


# ----------------- Staff/Admin: Manage Blood Requests -----------------
@staff_member_required
def manage_requests(request):
    requests = BloodRequest.objects.all().order_by("-requested_at")
    return render(request, "manage_requests.html", {"requests": requests})


@staff_member_required
def approve_request(request, req_id):
    req = get_object_or_404(BloodRequest, id=req_id)
    req.status = "Approved"
    req.save()
    return redirect("manage_requests")


@staff_member_required
def reject_request(request, req_id):
    req = get_object_or_404(BloodRequest, id=req_id)
    req.status = "Rejected"
    req.save()
    return redirect("manage_requests")


# ----------------- User: My Requests -----------------
@login_required
def my_requests(request):
    user_requests = BloodRequest.objects.filter(user=request.user)
    return render(request, 'my_requests.html', {'requests': user_requests})


# ----------------- User: My Donations -----------------









from django.contrib.auth.decorators import login_required

@login_required
def donated_persons(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.staff = request.user  # mark the staff
            donation.save()
            return redirect('donated_persons')  # reload the page
    else:
        form = DonationForm()
    
    donations = Donation.objects.all()
    return render(request, 'donated_persons.html', {'form': form, 'donations': donations})








@login_required
def my_donations(request):
    donations = Donation.objects.filter(user=request.user)
    return render(request, 'mydonations.html', {'donations': donations})

