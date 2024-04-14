import pyotp
from django.contrib import auth
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from app.core.constants import otp_purpose
from app.core.validators import validate_name, validate_password_format, validate_zip_code
from .models import User, UserOTP, UserProfile


# SERIALIZER VALIDATORS
unique_user_email = UniqueValidator(
    queryset=User.objects.all(), lookup="iexact", message="A user with this email already exists"
)


class UserOTPSerializer(serializers.Serializer):
    """
    Model serializer to accept otp purpose and send otp to user.
    """

    keys = otp_purpose
    send_options = (("mail", "mail"), ("sms", "sms"))

    otp_mode = serializers.CharField(required=True, write_only=True)
    send_mode = serializers.ChoiceField(
        choices=send_options,
        required=True,
        write_only=True,
        error_messages={"invalid_choice": "Please use a valid send mode e.g sms or mail"},
    )

    def validate(self, attrs):
        if not attrs["otp_mode"] in self.keys:
            raise serializers.ValidationError("The OTP mode submitted is not valid")

        user = self.context["request"].user
        otp_code = user.generate_otp(attrs["otp_mode"])

        subject = "OTP Verification Code for Gezapay"
        msg = f"Your verification code is {otp_code}"

        if attrs["send_mode"] == "mail":
            user.send_email(subject, msg)
        else:
            user.send_email(subject, msg)  # Change this when the SMS feature is implemented

        return attrs


class RegisterEmailSerializer(serializers.ModelSerializer):
    """
    Model Serializer for the User Registration View.
    Takes in email and password for Registration
    """

    email = serializers.EmailField(max_length=255, min_length=3, required=True, validators=[unique_user_email])
    password = serializers.CharField(
        max_length=50,
        min_length=8,
        write_only=True,
        required=True,
        validators=[validate_password, validate_password_format],
    )
    confirm_password = serializers.CharField(max_length=50, write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "confirm_password",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()

        return user


class RegisterSendSerializer(serializers.Serializer):
    """
    Serializer to accept email and send OTP code to new users for confirmation
    """

    email = serializers.EmailField(max_length=255, min_length=3, required=True, write_only=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"])
            if user.is_confirmed:
                raise serializers.ValidationError({"email": "This email has already been verified"})
            otp_code = user.generate_otp("auth")

            subject = "OTP Verification Code for Gezapay"
            message = f"Your verification code is {otp_code}"

            user.send_email(subject, message)

        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "This email has already been verified"})

        return attrs


class RegisterVerifySerializer(serializers.Serializer):
    """
    Model Serializer for the User Registration View.
    Takes in OTP code sent to email for verification
    """

    email = serializers.EmailField(max_length=255, min_length=3, required=True)
    otp_code = serializers.CharField(max_length=6, required=True)

    class Meta:
        fields = [
            "email",
            "otp_code",
        ]

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"])
            if user.is_confirmed:
                raise serializers.ValidationError({"email": "This email has already been verified"})
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User does not exist"})
        user = User.objects.get(email=attrs["email"])
        auth_secret_key = user.secret_keys["auth"]
        recent_otp = UserOTP.objects.filter(purpose="auth").order_by("-date_created").first()
        if recent_otp:
            if recent_otp.is_verified == False and recent_otp.code == attrs["otp_code"]:
                totp = pyotp.TOTP(auth_secret_key, interval=300)
                if totp.verify(attrs["otp_code"]) == True:
                    recent_otp.is_verified = True
                    recent_otp.save()
                    user.is_confirmed = True
                    user.is_ = True
                    user.save()
                    return attrs
                else:
                    raise serializers.ValidationError({"otp_code": "Expired OTP Code"})
            else:
                raise serializers.ValidationError({"otp_code": "Invalid OTP Code"})
        else:
            raise serializers.ValidationError({"otp_code": "Invalid OTP Code"})


class RegisterInfoSerializer(serializers.ModelSerializer):
    """
    Model Serializer to update and validate User Profile
    """

    first_name = serializers.CharField(max_length=50, required=True, validators=[validate_name])
    last_name = serializers.CharField(max_length=50, required=True, validators=[validate_name])
    phone = serializers.CharField(max_length=50, required=True)
    type = serializers.ChoiceField(choices=UserProfile.type_choices, required=True)
    gender = serializers.ChoiceField(choices=UserProfile.gender_choices, required=True)
    business = serializers.CharField(max_length=100, required=False)
    business_id = serializers.CharField(max_length=100, required=False)
    address = serializers.CharField(max_length=100, required=True)
    city = serializers.CharField(max_length=100, required=True)
    state = serializers.CharField(max_length=100, required=True)
    zipcode = serializers.CharField(max_length=10, required=True, validators=[validate_zip_code])
    country = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "phone",
            "type",
            "gender",
            "business",
            "business_id",
            "address",
            "city",
            "state",
            "zipcode",
            "country",
        ]

    def validate(self, attrs):
        if attrs["type"] == "BUSINESS" and "business" not in attrs.keys():
            raise serializers.ValidationError({"business": "This field is required for a business account"})
        if attrs["type"] == "BUSINESS" and "business_id" not in attrs.keys():
            raise serializers.ValidationError({"business_id": "This field is required for a business account"})

        return attrs

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.type = validated_data.get("type", instance.type)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.business = validated_data.get("business", instance.business)
        instance.business_id = validated_data.get("business_id", instance.business_id)
        instance.address = validated_data.get("address", instance.address)
        instance.city = validated_data.get("city", instance.city)
        instance.state = validated_data.get("state", instance.state)
        instance.zipcode = validated_data.get("zipcode", instance.zipcode)
        instance.country = validated_data.get("country", instance.country)
        instance.is_confirmed = True
        instance.save()

        return instance


class LoginSerializer(serializers.ModelSerializer):
    """
    Model Serializer for Log in view
    """

    email = serializers.EmailField(max_length=255, min_length=3, required=True)
    password = serializers.CharField(max_length=50, min_length=8, write_only=True, required=True)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "tokens",
        ]

    def get_tokens(self, obj):
        user = User.objects.get(email=obj["email"])

        return {"access": user.tokens()["access"], "refresh": user.tokens()["refresh"]}

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        user = auth.authenticate(email=email, password=password)

        if not user:
            try:
                user_email = User.objects.get(email=email)
                raise AuthenticationFailed({"message": "Invalid credentials", "password": "Wrong password"})
            except User.DoesNotExist:
                raise AuthenticationFailed({"message": "Invalid credentials", "email": "Invalid email"})
        if not user.is_confirmed:
            raise AuthenticationFailed({"message": "Email has not been verified", "email": "Unverified User"})
        if not user.is_active:
            raise AuthenticationFailed({"message": "Account has been blocked", "email": "Blocked User"})

        return {"email": user.email, "tokens": user.tokens}


class LogoutSerializer(serializers.Serializer):
    """
    Serializer class to handle logout and blacklisting of tokens
    """

    logout_options = (("current", "current"), ("all", "all"))

    access = serializers.CharField()
    refresh = serializers.CharField()
    mode = serializers.ChoiceField(
        choices=logout_options,
        required=True,
        write_only=True,
        error_messages={"invalid_choice": "Please use a valid send mode e.g current or all"},
    )

    def validate(self, attrs):
        if attrs["mode"] == "all":
            user = self.context["request"].user
            tokens = OutstandingToken.objects.filter(user=user)
            for token in tokens:
                t, _ = BlacklistedToken.objects.get_or_create(token=token)
        else:
            try:
                RefreshToken(attrs["refresh"]).blacklist()
            except TokenError:
                raise serializers.ValidationError({"refresh_token": "Token is invalid or expired"})

        return attrs
