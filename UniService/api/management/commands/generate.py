import math
import random
from datetime import date, timedelta

import tqdm
from accounts.models import User
from members_card.models import MemberCard
from api.util import current_total
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

BASE_ID: int = 1000000
Set_Usernames = set()


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
                user = User(
                    id=unique_id(CURRENT_USER_COUNT),
                    first_name=user[0],
                    last_name=user[1],
                    gender=user[2],
                    type=user[3],
                    address=user[4],
                    dob=user[5],
                    image=user_images(user[2]),
                )
                user.set_password(settings.USER_PASSWORD)
                user.save()
                card = MemberCard(active=True, user_id=user, photo=user.image)
                card.save()
        except KeyboardInterrupt:
            current_total()
            raise SystemExit
        current_total()


def unique_id(current_user_len) -> int:
    check_user_id = BASE_ID + current_user_len
    global CURRENT_USER_COUNT
    CURRENT_USER_COUNT += 1
    return check_user_id


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
    from mock_data.addressInfo import streettype, suburbs

    # from mock_data.addressInfo import streetnames
    from mock_data.male_firstname import names

    address = str(random.randrange(1, 210)) + " "
    address += random.choice(names) + " "
    address += random.choice(streettype) + ", "
    address += random.choice(suburbs)

    return address


def user_images(gender: str) -> str:
    """Generate a number to assign an image.
    https://raw.githubusercontent.com/Universally-University/backend/main/UniService/mock_data/UserImages/Female/image01.png
    Returns:
    str: image name"""
    max_female = 12
    max_male = 15
    imagestr = "https://raw.githubusercontent.com/Universally-University/backend/main/UniService/mock_data/UserImages/"
    match gender.upper()[0]:
        case "F":
            num = random.randint(1, max_female)
            imagestr += f"Female/image{num:02}.png"
        case "M":
            num = random.randint(1, max_male)
            imagestr += f"Male/image{num:02}.png"
        case _:
            raise NotImplementedError(f"Only Male or Female: {gender}")
    return imagestr


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
