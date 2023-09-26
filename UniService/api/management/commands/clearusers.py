import math
import random
from datetime import date, timedelta

import api.models as api
from accounts.models import User
from api.util import current_total
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Clears Users, if all are False, it will clear all."

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--undergraduate",
            action="store_true",
            help="Clear all undergraduates. Default: False",
        )
        parser.add_argument(
            "-p",
            "--postgraduate",
            action="store_true",
            help="Clear all postgraduates. Default: False",
        )
        parser.add_argument(
            "-s",
            "--staff",
            action="store_true",
            help="Clear all staff. Default: False",
        )

    def handle(
        self, undergraduate: bool, postgraduate: bool, staff: bool, *args, **options
    ):
        if not (undergraduate | postgraduate | staff):
            undergraduate = True
            postgraduate = True
            staff = True

        if undergraduate:
            User.objects.filter(type="U").delete()
        if postgraduate:
            User.objects.filter(type="P").delete()
        if staff:
            User.objects.filter(type="S").delete()
        current_total()
            
