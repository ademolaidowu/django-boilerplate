import pyotp
from django.db import models
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from app.core.models import UUIDModel, TimeStampedModel, OTPSecretModel
from app.core.validators import validate_zip_code
from .managers import UserManager


class User(UUIDModel, AbstractBaseUser, PermissionsMixin, OTPSecretModel, TimeStampedModel):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Email and password are required. Other fields are optional.
    """

    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )
    is_confirmed = models.BooleanField(
        _("confirmed"),
        default=False,
        help_text=_("Designates whether this user's email has been confirmed"),
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-date_created"]

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs):
        if not self.pk:
            new_keys = self.initiate_all_sk()
            self.secret_keys = new_keys
        super().save(*args, **kwargs)

    @property
    def full_name(self) -> str:
        """
        Return the first_name plus the last_name, with a space in between
        or Unconfirmed User if email has not been confirmed yet
        """
        if self.is_confirmed == False:
            return "Unconfirmed User"
        full_name = "%s %s" % (self.profile.first_name, self.profile.last_name)

        return full_name.strip()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def send_email(self, subject, msg):
        """Send emails with no attachment"""
        email = EmailMessage(subject=subject, body=msg, to=[self.email])
        email.send()

    def generate_otp(self, purpose: str) -> str:
        try:
            self.secret_keys[purpose]
        except:
            self.create_all_sk()
        purpose_sk = self.secret_keys[purpose]
        otp = pyotp.TOTP(purpose_sk, interval=300)  # Ensure the interval passed here is the same during verification
        otp_code = otp.now()
        UserOTP.objects.create(user=self, purpose=purpose, code=otp_code)

        return otp_code


class UserProfile(UUIDModel, TimeStampedModel):
    """
    A class implementing a fully featured User Profile with
    unique foreign key relationship with the User Model
    """

    # Choices
    gender_choices = (
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE"),
        ("OTHERS", "OTHERS"),
    )

    type_choices = (
        ("INDIVIDUAL", "INDIVIDUAL"),
        ("BUSINESS", "BUSINESS"),
    )

    verification_choices = (
        ("UNVERIFIED", "UNVERIFIED"),
        ("PENDING", "PENDING"),
        ("VERIFIED", "VERIFIED"),
    )

    user = models.OneToOneField(User, to_field="id", on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(_("first name"), max_length=150, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True, null=True)
    phone = models.CharField(_("phone number"), max_length=16, blank=True, null=True)
    gender = models.CharField(_("gender"), max_length=6, choices=gender_choices, default="OTHERS")
    type = models.CharField(_("account type"), max_length=10, choices=type_choices, default="INDIVIDUAL")
    is_confirmed = models.BooleanField(
        _("confirmed"),
        default=False,
        help_text=_("Designates whether this user has completed registration process."),
    )
    is_verified = models.CharField(
        _("verified"),
        max_length=10,
        choices=verification_choices,
        default="UNVERIFIED",
        help_text=_("Designates whether this user's KYC has been completed and account can make transactions."),
    )
    address = models.CharField(_("address"), max_length=255, blank=True, null=True)
    city = models.CharField(_("city"), max_length=100, blank=True, null=True)
    state = models.CharField(_("state"), max_length=50, blank=True, null=True)
    zipcode = models.CharField(_("zip code"), max_length=10, blank=True, null=True, validators=[validate_zip_code])
    country = models.CharField(_("country"), max_length=50, blank=True, null=True)
    business = models.CharField(_("business name"), max_length=100, blank=True, null=True)
    business_id = models.CharField(_("business id"), max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ["user", "business_id"]
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
        ordering = ["-date_created"]

    @property
    def full_name(self) -> str:
        """Return the first_name plus the last_name, with a space in between."""
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self) -> str:
        if self.type == "business":
            return f"{self.business}'s Profile"
        return f"{self.user.full_name}'s Profile"

    def clean(self):
        """
        Model validation to ensure business and business_id are not blank if type is BUSINESS.
        """
        if self.type == "BUSINESS" and not self.business:
            raise ValidationError({"business": "This field is required for business account"})
        if self.type == "BUSINESS" and not self.business_id:
            raise ValidationError({"business_id": "This field is required for business account"})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class UserOTP(TimeStampedModel):
    """
    A class to implement storage of created OTPs for several purposes in the
    application.
    """

    user = models.ForeignKey(User, to_field="id", on_delete=models.CASCADE, related_name="otp")
    code = models.CharField(_("OTP code"), max_length=6)
    purpose = models.CharField(_("OTP purpose"), max_length=50)
    is_verified = models.BooleanField(
        _("verified"),
        default=False,
        help_text=_("Designates whether this OTP has been used by the user."),
    )

    class Meta:
        verbose_name = _("User OTP")
        verbose_name_plural = _("User OTP")
        ordering = ["-date_created"]

    def __str__(self) -> str:
        return f"{self.user.id}"
