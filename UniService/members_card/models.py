from datetime import date, timedelta
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class MemberCard(models.Model):
    card_num = models.AutoField(_("Card Number"), primary_key=True)
    user_id = models.ForeignKey("accounts.User", verbose_name=_("User ID"), on_delete=models.CASCADE)
    issued_date = models.DateField(_("Issued on"), auto_now_add=True)
    expiry_date = models.DateField(
        _("Expires on"), default=(date.today() + timedelta(days=365))
    )
