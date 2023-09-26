from accounts.models import User


def current_total():
    """Prints the current user count.
    
    Example:
        Current Total
        U: 697
        P: 0
        S: 0
    """
    print("Current Total")
    print(f"U: {User.objects.filter(type='U').count()}")
    print(f"P: {User.objects.filter(type='P').count()}")
    print(f"S: {User.objects.filter(type='S').count()}")
