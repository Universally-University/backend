from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, id=None, password=None, email=None, *args, **extra_fields):
        if not id:
            id = User.objects.filter("A").count() + 1
        if not password:
            raise ValueError("Password must be included.")
        user: User = self.model(id=id, **extra_fields)
        if email:
            user.email = self.normalize_email(email)

        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, id=1, password=None, *args, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user: User = self.create_user(id=id, password=password, **extra_fields)
        user.type = "A"
        user.is_staff = True
        user.is_superuser = True
        user.save(update_fields=["is_staff", "is_active", "is_superuser", "type"])
        return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    id = models.IntegerField(_("User ID"), primary_key=True, auto_created=True)
    USERNAME_FIELD = "id"
    first_name = models.CharField(
        _("First Name"), max_length=255, null=True, blank=True
    )
    last_name = models.CharField(_("Last Name"), max_length=255, null=True, blank=True)
    dob = models.DateField(_("Date of Birth"), null=True, blank=True)
    address = models.CharField(_("Address"), max_length=300, null=True, blank=True)
    type = models.CharField(
        _("Type"),
        max_length=30,
        choices=(
            ("U", "Undergraduate"),
            ("P", "Postgraduate"),
            ("S", "Staff"),
            ("A", "Admin"),
        ),
    )
    gender = models.CharField(
        _("Gender"),
        max_length=6,
        choices=(("M", "Male"), ("F", "Female")),
        null=True,
        blank=True,
    )
    image= models.URLField(verbose_name=_("User Image"))
    # Permissions
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        printable_items=[self.gender, self.dob, self.address]
        return f"{self.type} {self.id}: {self.first_name} {self.last_name}{', ' if all(printable_items) else ''}{', '.join([str(item) for item in printable_items if item])}"

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_absolute_url(self):
        return reverse("User_detail", kwargs={"pk": self.pk})
