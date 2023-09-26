import math
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
import random
from datetime import timedelta, date
import api.models as api
from accounts.models import User
from django.conf import settings
import tqdm
from api.util import current_total

BASE_ID: int = 1000000


class Command(BaseCommand):
    help = "Generates data"

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--undergraduate",
            type=int,
            default=0,
            required=False,
            help="Number of undergraduate students to generate. Default: 10000",
        )
        parser.add_argument(
            "-p",
            "--postgraduate",
            type=int,
            default=0,
            required=False,
            help="Number of postgraduate students to generate. Default: 10000",
        )
        parser.add_argument(
            "-s",
            "--staff",
            type=int,
            default=0,
            required=False,
            help="Number of staff to generate. Default: 100",
        )

    def handle(
        self, undergraduate: int, postgraduate: int, staff: int, *args, **options
    ):
        global CURRENT_USER_COUNT
        CURRENT_USER_COUNT = User.objects.all().count()
        try:
            for user in tqdm.tqdm(
                [
                    *name_list(undergraduate, "U"),
                    *name_list(postgraduate, "P"),
                    *name_list(staff, "S", min_age=25, max_age=65),
                ]
            ):
                User(
                    id=unique_id(CURRENT_USER_COUNT),
                    first_name=user[0],
                    last_name=user[1],
                    gender=user[2],
                    type=user[3],
                    address=user[4],
                    dob=user[5],
                ).save()
        except KeyboardInterrupt:
            current_total()
            raise SystemExit
        current_total()


def unique_id(current_user_len) -> int:
    check_user_id = BASE_ID + current_user_len
    # while True:
    # temp_user_count = User.objects.filter(id=check_user_id).count()
    global CURRENT_USER_COUNT
    CURRENT_USER_COUNT += 1
    return check_user_id
    # check_user_id += 1


def name_list(
    x: int,
    name_type: str,
    gender_split: float = 0.5,
    min_age: int = 18,
    max_age: int = 80,
) -> list[tuple[str, str, str, str, str, date]]:
    """Generates a list of students or staff with a set gender split.

    Args:
        x (int): Number of names.
        name_type (str): Type of name i.e. "U" for undergrad, "P" for postgrad or "S" for staff.
        gender_split (float, optional): The ratio of males in group, 0 would be 100% females and vice versa. Defaults to 0.5.
        min_age (int, optional): Minimum age. Defaults to 18.
        max_age (int, optional): Maximum age. Defaults to 80.

    Returns:
        list[tuple[str, str, str, str, str, date]]: List of names
                    with list[tuple[firstname, lastname, gender, name_type, address, DoB].
    """
    ret_list = [
        *names(math.floor(x * gender_split), "male"),
        *names(math.ceil(x * (1 - gender_split)), "female"),
    ]
    ret_list = [
        (*person, name_type, address(), dob(min_age, max_age)) for person in ret_list
    ]
    return ret_list


def names(x: int, gender: str) -> list[tuple[str, str, str]]:
    """Generates a list of names.

    Args:
        x (int): Number of names to generate
        gender (str): Gender for the names, "female" or "male".

    Raises:
        CommandError: Invalid x or gender.

    Returns:
        list[tuple[str, str, str]]: List of names of the specified gender.
    """
    if not isinstance(x, int):
        raise CommandError(f"x needs to be an int, x: {x}")
    match gender.lower():
        case "female":
            from mock_data.female_firstname import names
        case "male":
            from mock_data.male_firstname import names
        case _:
            raise CommandError("Gender needs to be either male or female")
    from mock_data.lastname import lastnames

    gender = gender.upper()[0]
    name_list: list[tuple[str, str]] = []
    for _ in range(x):
        name_list.append(
            (
                random.choice(names).capitalize(),
                random.choice(lastnames).capitalize(),
                gender,
            )
        )
    return name_list


def address() -> str:
    """Generate a random address.

    Returns:
        str: Random Address.
    """

    return "42 Wallaby Way, Sydney, NSW, 2000"


def dob(min_age: int = 18, max_age: int = 80) -> date:
    """Date of Birth

    Generates a random DoB between the min_age and the max_age.

    Args:
        min_age (int, optional): Minimum age. Defaults to 18.
        max_age (int, optional): Maximum age. Defaults to 80.

    Returns:
        date: Date of Birth
    """
    days = random.randrange(min_age * 365, max_age * 365)
    return date.today() - timedelta(days=days)


if __name__ == "__main__":
    print(names(10, gender="female"))
