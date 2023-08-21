from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _


class Account(models.Model):
    id = models.IntegerField(_("User ID"), primary_key=True, auto_created=True)
    first_name = models.CharField(_("First Name"), max_length=255)
    last_name = models.CharField(_("Last Name"), max_length=255)
    dob = models.DateField(_("Date of Birth"))
    contact = models.CharField(_("Contact"), max_length=100)
    address = models.CharField(_("Address"), max_length=300)
    type = models.CharField(
        _("Type"),
        max_length=30,
        choices=(("U", "Undergraduate"), ("P", "Postgraduate"), ("S", "Staff")),
    )
    is_active = models.BooleanField(_("Is active"))

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("User_detail", kwargs={"pk": self.pk})
