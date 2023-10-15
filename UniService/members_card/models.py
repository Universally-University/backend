from datetime import date, timedelta
import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"member_photo/{instance.user_id}/{datetime.datetime.isoformat(sep='T', timespec='auto')}"


# Create your models here.
class MemberCard(models.Model):
    card_num = models.AutoField(_("Card Number"), primary_key=True)
    user_id = models.ForeignKey(
        "accounts.User", verbose_name=_("User ID"), on_delete=models.CASCADE
    )
    issued_date = models.DateField(_("Issued on"), auto_now_add=True)
    expiry_date = models.DateField(
        _("Expires on"), default=(date.today() + timedelta(days=365))
    )
    active = models.BooleanField(_("Active Card"), default=True)
    photo = models.TextField(
        verbose_name=_("User Image"),
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.user_id.id}{self.card_num}: {"Active, " if self.active else ""}{self.expiry_date}'
