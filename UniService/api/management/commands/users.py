import math
import random
from datetime import date, timedelta

import api.models as api
from accounts.models import User
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Print user count or list users."

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--undergraduate",
            action='store_true',
            help="Print undergraduate count. Default: True",
        )
        parser.add_argument(
            "-p",
            "--postgraduate",
            action='store_true',
            help="Print postgraduate count. Default: True",
        )
        parser.add_argument(
            "-s",
            "--staff",
            action='store_true',
            help="Print staff count. Default: True",
        )
        parser.add_argument(
            "-P",
            "--print_list",
            action='store_true',
            help="Print user list with the u, p, and s flags in mind. Default: True",
        )

    def handle(
        self, undergraduate:bool, postgraduate:bool, staff:bool,print_list:bool, *args, **options
    ):
        if not (undergraduate | postgraduate | staff):
            undergraduate = True
            postgraduate = True
            staff = True

        if not print_list:
            print("Total")
            if undergraduate:    
                print(f"U: {User.objects.filter(type='U').count()}")
            if postgraduate:    
                print(f"P: {User.objects.filter(type='P').count()}")
            if staff:    
                print(f"S: {User.objects.filter(type='S').count()}")
        else:
            if undergraduate:    
                print("Undergraduates:")
                [print("\t"+ str(u)) for u in User.objects.filter(type='U')]
            if postgraduate:    
                print("Postgraduates:")
                [print("\t"+ str(u)) for u in User.objects.filter(type='P')]
            if staff:    
                print("Staff:")
                [print("\t"+ str(u)) for u in User.objects.filter(type='S')]
