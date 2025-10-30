from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # dashboards
    path("user-dashboard/", views.user_dashboard, name="user_dashboard"),
    path("staff-dashboard/", views.staff_dashboard, name="staff_dashboard"),

    # donor
    path('donate-blood/', views.donate_blood, name='donate_blood'),
    path('donors/', views.donor_list, name='donor_list'),

    # extra pages
    path("available-blood/", views.available_blood, name="available_blood"),
    path("campaigns/", views.campaigns, name="campaigns"),
    path("announcements/", views.announcements, name="announcements"),

    # Staff: Blood Inventory
    path("staff-blood-inventory/", views.staff_blood_inventory, name="staff_blood_inventory"),
    path("staff-blood-inventory/add/", views.add_blood_inventory, name="add_blood_inventory"),
    path("staff-blood-inventory/edit/<int:pk>/", views.edit_blood_inventory, name="edit_blood_inventory"),

    # User: Blood Request
    path("request-blood/", views.request_blood, name="request_blood"),

    # Staff/Admin: Manage Requests
    path("manage-requests/", views.manage_requests, name="manage_requests"),
    path("my-requests/", views.my_requests, name="my_requests"),
    path("approve-request/<int:req_id>/", views.approve_request, name="approve_request"),
    path("reject-request/<int:req_id>/", views.reject_request, name="reject_request"),


    path('staff/donated-persons/', views.donated_persons, name='donated_persons'),
    path('user/my-donations/', views.my_donations, name='my_donations'),

     
]




