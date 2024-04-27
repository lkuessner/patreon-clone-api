from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model.

    This model extends the default Django user model to include additional fields.
    """

    username = models.CharField(_("Username"), max_length=255, unique=True)
    first_name = models.CharField(_("First Name"), max_length=255)
    last_name = models.CharField(_("Last Name"), max_length=255)
    password = models.CharField(_("Password"), max_length=255)

    def __str__(self):
        return self.username


class Profile(models.Model):
    """
    Profile model.

    This model represents a user's profile information.
    """

    user = models.OneToOneField(
        User,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="profile",
        blank=True,
        null=True,
    )

    email = models.EmailField(_("Email"), unique=True)
    email_verified = models.BooleanField(_("Is email verified"), default=False)

    dob = models.DateField()
    stripe_id = models.CharField(_("Stripe ID"), max_length=255, blank=True, null=True)

    profile_image = models.ImageField(
        _("Profile Image"), upload_to="profile_images/", blank=True, null=True
    )
    is_social = models.BooleanField(_("Is social"), default=False)
    google_login_token = models.CharField(
        _("Google Login Token"), max_length=255, blank=True, null=True
    )
    facebook_login_token = models.CharField(
        _("Facebook Login Token"), max_length=255, blank=True, null=True
    )

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    created_by = models.ForeignKey(
        "self",
        verbose_name=_("Created by"),
        on_delete=models.CASCADE,
        related_name="users",
        blank=True,
        null=True,
    )
    modified_at = models.DateTimeField(_("Modified at"), auto_now=True)
    modified_by = models.ForeignKey(
        "self",
        verbose_name=_("Created by"),
        on_delete=models.CASCADE,
        related_name="users_modified",
        blank=True,
        null=True,
    )
    deleted_at = models.DateTimeField(_("Deleted at"), blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
