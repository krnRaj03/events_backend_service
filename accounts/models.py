from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password, make_password

# from .utilities import generate_otp,send_email_via_sendinblue
import uuid


# Create your models here.
class CustomUser(AbstractBaseUser):
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )
    JOB_TITLE_CHOICES = (
        ("manager", "Manager"),
        ("developer", "Developer"),
        ("designer", "Designer"),
        ("analyst", "Analyst"),
        ("tester", "Tester"),
        ("hr", "HR"),
        ("accountant", "Accountant"),
        ("sales", "Sales"),
        ("student", "Student"),
        ("other", "Other"),
    )
    ROLE_CHOICES = (
        ("speaker", "Speaker"),
        ("moderator", "Moderator"),
        ("guest", "Guest"),
        ("sponsor", "Sponsor"),
        ("organizer", "Organizer"),
    )
    username = None
    email = models.EmailField(unique=True)
    password_reset_token = models.CharField(max_length=100, blank=True)
    email_otp = models.CharField(max_length=6, blank=True)
    mobile_no = models.CharField(max_length=10, blank=True)
    mobile_otp = models.CharField(max_length=6, blank=True)

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(_("dateofbirth"), blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    is_active = models.BooleanField(_("active"), default=True)
    job_title = models.CharField(max_length=20, choices=JOB_TITLE_CHOICES, blank=True)
    is_user = models.BooleanField(_("user status"), default=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_superuser = models.BooleanField(default=False)

    status = models.CharField(max_length=20, blank=True)
    # signup_pending,signup_done,deleted,blocked
    date_created = models.DateTimeField(auto_now_add=True)
    user_image = models.URLField(max_length=200, blank=True)
    address_line1 = models.CharField(max_length=100, blank=True)
    address_line2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=100, blank=True)

    linkedin_url = models.URLField(max_length=200, blank=True)
    twitter_url = models.URLField(max_length=200, blank=True)
    facebook_url = models.URLField(max_length=200, blank=True)
    instagram_url = models.URLField(max_length=200, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    panel_no = models.CharField(max_length=100, blank=True)
    topic = models.CharField(max_length=100, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_full_name(self):
        """
        Returns the user's full name.
        """
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        """
        Returns the user's short name.
        """
        return self.first_name

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the given permission.
        """
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has permissions to view the app with the given label.
        """
        return True

    def set_password(self, raw_password):
        """
        Sets the user's password to the given raw password.
        """
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Checks if the given raw password matches the user's stored password hash.
        """
        return check_password(raw_password, self.password)
