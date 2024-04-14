import uuid
import pyotp
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .constants import otp_purpose


class UUIDModel(models.Model):
    """An abstract base class for UUID fields."""

    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """An abstract base class for timestamp fields."""

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(default=timezone.now)
    date_deleted = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class OTPSecretModel(models.Model):
    """
    An abstract base class for generating OTP secret keys for
    generating OTPs for the User Model.
    """

    keys = otp_purpose
    secret_keys = models.JSONField(default=dict)

    class Meta:
        abstract = True

    def initiate_all_sk(self) -> dict:
        """
        Function to generate all secret keys on User Model for OTP generation,
        to be invoked on user creation.
        """
        new_keys = {}
        for purpose in self.keys:
            otp_secret = pyotp.random_base32()
            new_keys[purpose] = otp_secret

        return new_keys

    def create_all_sk(self) -> dict:
        """
        Function to generate all secret keys on User Model for OTP generation,
        to be invoked when called.
        """
        new_keys = {}
        for purpose in self.keys:
            otp_secret = pyotp.random_base32()
            new_keys[purpose] = otp_secret

        self.secret_keys = new_keys
        self.save()

        return self.secret_keys

    def modify_sk(self, purpose: str) -> dict:
        """
        Function to add or edit a secret key on User Model for OTP generation.
        """
        otp_secret = pyotp.random_base32()
        self.secret_keys[purpose] = otp_secret
        self.save()

        return self.secret_keys

    def remove_all_sk(self) -> dict:
        """
        Function to remove all secret keys on User Model for OTP generation.
        """
        self.secret_keys = {}
        self.save()

        return self.secret_keys
