from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(models.Model):
    id = models.IntegerField(_("User ID"), primary_key=True, auto_created=True)
    first_name = models.CharField(_("First Name"), max_length=255)
    last_name = models.CharField(_("Last Name"), max_length=255)
    dob = models.DateField(_("Date of Birth"))
    address = models.CharField(_("Address"), max_length=300)
    type = models.CharField(
        _("Type"),
        max_length=30,
        choices=(("U", "Undergraduate"), ("P", "Postgraduate"), ("S", "Staff")),
    )
    gender = models.CharField(
        _("Gender"), max_length=6, choices=(("M", "Male"), ("F", "Female"))
    )
    is_active = models.BooleanField(_("Is active"), default=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.type} {self.id}: {self.first_name} {self.last_name}, {self.dob}"
    

    def get_absolute_url(self):
        return reverse("User_detail", kwargs={"pk": self.pk})
