from application.models import create_usage


def test_new_usage():
    """
    GIVEN a Usage model
    WHEN a new Usage is created
    THEN check the computer id is valid, player id is valid, and start timestamp is initiated
    """
    new_usage = create_usage()
