from typing import Tuple
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask import current_app as app
from application import apscheduler, cache
from . import db, login_manager
from flask_login import UserMixin
import json
from datetime import date, datetime, timezone, timedelta
import zoneinfo
import os
import time
import re


NUM_COMPUTERS = 26

COMP_STATUS_KEY = 'computer_statuses'
TIMESTAMP_KEY = 'computer_timestamps'
COMP_USAGES_KEY = 'computer_usages'
SAVED_JOBS_KEY = 'computer_jobs'

IN_USE_STATUS_CODE = 1
DISABLED_STATUS_CODE = -1
EMPTY_STATUS_CODE = 0


current_active_computers = [None] * NUM_COMPUTERS
computer_statuses = [0] * 26
user_info_keys = ('first_name', 'last_name',
                  'email_prefix', 'role', 'team', 'user_id')

# Intialize timezone
pacifictz = zoneinfo.ZoneInfo("US/Pacific")

# redis_host = os.environ.get('REDIS_HOST')
# redis_pass = os.environ.get('REDIS_PASSWORD')
# redis_port = int(os.environ.get('REDIS_PORT'))

# my_redis = redis.Redis(host=redis_host, port=redis_port,
#                        password=redis_pass, ssl=True, ssl_cert_reqs=None, db=0)
# my_redis = redis.Redis()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    Loads existing User table from PostgreSQL
    """
    __table__ = db.Model.metadata.tables['public.users']

    def get_id(self):
        return (self.user_id)

    def has_permissions(self, perms):
        return perms in self.permissions


class Usage(db.Model):
    """
    Loads existing User table from PostgreSQL
    """
    __table__ = db.Model.metadata.tables['public.usages']


class EsportUsage(db.Model):
    """
    Loads existing Esports Usages table from PostgreSQL
    """
    __table__ = db.Model.metadata.tables['public.esports_usages']


class ComputerStatus(db.Model):
    """
    Loads existing Esports Usages table from PostgreSQL
    """
    __table__ = db.Model.metadata.tables['public.computer_statuses']


class Player(db.Model):
    """
    Loads existing Player table from PostgreSQL
    """
    __table__ = db.Model.metadata.tables['public.players']

# class DailySchedules(db.Model):
#     """
#     Loads existing User table from PostgreSQL
#     """
#     __table__ = db.Model.metadata.tables['public.daily_schedules']


# class WeeklySchedules(db.Model):
#     """
#     Loads existing User table from PostgreSQL
#     """
#     __table__ = db.Model.metadata.tables['public.weekly_schedules']


def json_response(status_message: str, status_code: int, body=None):
    if body:
        return json.dumps({'statusMessage': status_message,
                           'status': status_code,
                           'body': body})
    else:
        return json.dumps({'statusMessage': status_message,
                           'status': status_code})


def valid_ucsd_email(email):
    pattern = re.compile('^[A-Za-z0-9]*@ucsd\.edu$')
    return re.fullmatch(pattern, email)


def get_pc_status(computer_id: int):
    """
    Returns the pc object at the current computer id.
    None if the pc doesn't exist
    """
    computer = ComputerStatus.query.filter_by(computer_id=computer_id).first()
    return computer


def set_pc_in_use(computer_id: int, email=None):
    """
    A method that sets the given computer id to in use.

    Parameter(s):
        comp_id (int): The id of the computer to set to in use.
    """
    # Make sure the computer id is within bounds
    if computer_id <= 0 or computer_id > NUM_COMPUTERS:
        return json_response(f'Computer id {computer_id} is out of range', 400)

    comp_index = computer_id - 1

    start_timestamp_seconds = None

    # Get the current computer from db
    computer = get_pc_status(computer_id)

    if computer.status == DISABLED_STATUS_CODE:
        return json_response(f"Couldn't set {computer_id} in use because it is disabled.", 400,
                             body={'usageId': DISABLED_STATUS_CODE})

     # If already enabled, do nothing
    print(computer.status)
    if computer.status >= IN_USE_STATUS_CODE:
        if email:
            body = {'usageId': computer.status,
                    'email': computer.email}
        else:
            body = {'usageId': computer.status,
                    'startTimestampSeconds': computer.start_timestamp}
        return json_response(f'Computer {computer_id} already in use.', 400, body=body)

    # If there is an email provided, we are in esports and don't have a timer
    if email:
        # Make sure the email is formatted correctly
        if not valid_ucsd_email(email=email):
            return json_response(f'Email: {email} is not a valid ucsd email.', 400)

        # Query for the users email
        player = query_player(email)

        if player == None:
            return json_response(f"Player with email: {email} doesn't exist!", 400)

        # Create new usage
        new_usage = create_usage(player.player_id, computer_id, esports=True)
        print(new_usage)

    else:
        # query for open rec user id
        open_rec_user = query_user('openrec@ucsd.edu')

        # Create new usage
        new_usage = create_usage(open_rec_user.user_id, computer_id)

        # Change timezone to utc
        start_timestamp_seconds = datetime.timestamp(new_usage.start_timestamp.replace(
            tzinfo=timezone.utc))

        # Create auto end time 8 hours later
        # one_min_seconds = 60
        eight_hours_seconds = (1/4) * 60 * 60  # 8 hours * 60 min * 60 sec
        end_datetime = start_timestamp_seconds + eight_hours_seconds
        print(datetime.fromtimestamp(end_datetime))
        # Start timer for 8 hour auto ending of session
        job_id = f'auto_end_{new_usage.usage_id}'
        apscheduler.add_job(id=job_id, func=end_pc_use,
                            run_date=datetime.fromtimestamp(end_datetime),
                            kwargs={'usage_id': new_usage.usage_id,
                                    'computer_id': computer_id,
                                    'esports': False,
                                    'scheduled': True})

    # Change the current status of the computer in Postgres
    worked = change_pc_status(
        computer, new_usage.usage_id, new_usage.start_timestamp, email)

    if not worked:
        return worked

    if email:
        body = {'usageId': new_usage.usage_id}
    else:
        body = {'usageId': new_usage.usage_id,
                'startTimestampSeconds': start_timestamp_seconds}
    print(body)

    # Delete the current cache pc usages if it exists
    try:
        cache.clear()
        print('deleted db_pc_usages from cache')
    except:
        print("db_pc_usages not in cache")

    return json_response(f'Computer {computer_id} now in use!', 200, body)


def change_pc_status(computer: ComputerStatus, status: int, start_timestamp=None, email=None):
    computer.status = status
    computer.start_timestamp = start_timestamp
    computer.email = email
    try:
        db.session.commit()
    except IntegrityError as ie:
        db.session.rollback()
        return ie.detail
    return True


def end_usage_change_status(usage_id: int, computer_id: int, esports=False):
    """
    A method to end the current computer usage and also changes the status of the pc.

    Parameter(s):
        usage_id (int): The usage id to end.
        computer_id (int): The id of the computer to change status.
        esports (bool): Whether the session to end was esports (default False).
    """
    # Query for the usage and the computer
    usage = query_usage(usage_id, esports)
    computer = get_pc_status(computer_id)

    # Update the parameters
    if usage == None:
        return json_response("Usage id not found.", 400)

    if computer == None:
        return json_response("Computer id not found.", 400)

    # Set the attributes
    setattr(usage, 'end_timestamp', datetime.utcnow())
    setattr(computer, 'status', EMPTY_STATUS_CODE)
    setattr(computer, 'start_timestamp', None)
    setattr(computer, 'email', None)

    try:
        db.session.commit()
        return True
    except IntegrityError as ie:
        db.session.rollback()
        return json_response("Failed to connect to database.", 400)


def end_pc_use(usage_id: int, computer_id: int, esports=False, scheduled=False):
    """
    A method that ends the given computer usage.

    Parameter(s):
        usage_id (int): The usage id to end.
    """
    # Get the current computer from db
    computer = get_pc_status(computer_id)

    if computer.status == DISABLED_STATUS_CODE:
        return json_response(f"Couldn't end computer {computer_id} because it is disabled.", 400,
                             body={'usageId': DISABLED_STATUS_CODE})

     # If already enabled, do nothing
    if computer.status != usage_id:
        if esports:
            body = {'usageId': computer.status,
                    'email': computer.email}
        else:
            body = {'usageId': computer.status,
                    'startTimestampSeconds': computer.start_timestamp}
        return json_response(f'Old computer use already ended at computer {computer_id}.', 400, body=body)

    if esports:
        # attempt to end usage and change status on db
        ended = end_usage_change_status(usage_id, computer_id, esports)
        if ended != True:
            return ended

        # Delete the current cache pc usages if it exists
        try:
            cache.clear()
        except:
            print("db_pc_usages not in cache")

        return json_response("Computer session ended!", 200)

    app = apscheduler.app
    with app.app_context():

        # Check usage id is valid
        if usage_id == None:
            return json_response("Usage id not provided.", 400)

        # Make sure the computer id is within bounds
        if computer_id <= 0 or computer_id > NUM_COMPUTERS:
            return json_response(f'Computer id {computer_id} is out of range', 400)

        # attempt to end usage on database
        ended_usage = end_usage_change_status(usage_id, computer_id, esports)
        if ended_usage != True:
            return ended_usage

        if not scheduled:
            # End job_id
            job_id = f'auto_end_{usage_id}'
            apscheduler.remove_job(job_id)
        print("Successfully ended session")

        return json_response("Computer session ended!", 200)


def end_usage(usage_id: int, esports=False):
    # End session on database with current timestamp
    usage = query_usage(usage_id, esports)

    if usage == None:
        return json_response("Usage id not found.", 400)
    setattr(usage, 'end_timestamp', datetime.utcnow())
    # db.session.merge(usage)

    try:
        db.session.commit()
        return True
    except IntegrityError as ie:
        db.session.rollback()
        return json_response("Failed to connect to database.", 400)


def reset_pc_statuses():
    """
    A method that resets (sets all entries to 0) all pc statuses.
    """
    for i in range(0, NUM_COMPUTERS):
        computer = get_pc_status(i+1)
        change_pc_status(computer, EMPTY_STATUS_CODE, None, None)


reset_pc_statuses()


@cache.memoize(timeout=30)
def get_db_pc_usages(esports=False):
    """
    Returns a list of current esports usage statuses
    and if esports=False, the start timestamps of each computer as well.
    """
    print("in db function")
    if esports:
        usages = ComputerStatus.query.with_entities(
            ComputerStatus.computer_id, ComputerStatus.status, ComputerStatus.email
        ).order_by(ComputerStatus.computer_id).all()
    else:
        usages = ComputerStatus.query.with_entities(
            ComputerStatus.computer_id, ComputerStatus.status, ComputerStatus.start_timestamp
        ).order_by(ComputerStatus.computer_id).all()
    return [list(x) for x in usages]


def get_pc_statuses():
    # Get the complete db usages
    complete_statuses = get_db_pc_usages()

    print(complete_statuses)

    return [x[1] for x in complete_statuses]


def disable_computers(computer_ids: set):
    """
    Updates the disabled of each computer in computer ids
    """
    disabled = []
    enabled = []
    local_statuses = []
    for i in range(len(current_active_computers)):
        comp_id = i + 1
        if comp_id in computer_ids:
            if current_active_computers[comp_id-1] != -1:
                current_active_computers[i] = -1
                disabled.append(comp_id)
                local_statuses.append(-1)
                # Change status code to in use
                computer_statuses[comp_id-1] = DISABLED_STATUS_CODE

        elif current_active_computers[i] == -1:
            current_active_computers[comp_id-1] = None
            enabled.append(comp_id)
            # Change status code to in use
            computer_statuses[i] = EMPTY_STATUS_CODE
            local_statuses.append(0)
        elif current_active_computers[i] == None:
            # Change status code to in use
            computer_statuses[i] = EMPTY_STATUS_CODE
            local_statuses.append(0)
        else:
            local_statuses.append(1)
    print(current_active_computers)

    return json.dumps({'statusMessage': f"Successfully disabled {disabled}. Re-enabled {enabled} because there are people active.",
                       'status': 200,
                       'body': {'activeComputers': computer_statuses}})


def get_days_usages():
    """
    Returns the usages from today as a list of Usages and today's date.
    """
    today = datetime.now(pacifictz).date()
    usages = Usage.query.filter(Usage.start_timestamp >= today).all()
    return usages, today


def query_users(user_ids: set):
    """
    Returns the information of the given user ids. None if the user doesn't exist.
    """
    return User.query.filter(User.user_id.in_(user_ids)).all()


def query_user(email: str) -> User:
    """
    Returns a user with the given email if they exist. Returns None otherwise.

    Parameter(s):
        email(str): A given ucsd email to check existence in user table of.
    """
    user = User.query.filter_by(email=email).first()
    return user


def query_player(email: str, player_id=None) -> Player:
    """
    Returns a user with the given email or player id if they exist. Returns None otherwise.

    Parameter(s):
        email(str): A given ucsd email to check existence in user table of.
    """
    if email:
        player = Player.query.filter_by(email=email).first()
    elif player_id:
        player = Player.query.filter_by(player_id=player_id).first()
    else:
        return None
    return player


def create_user(user_dict: dict) -> User:
    """
    Returns a newly created user with the given values and adds that user to the database if that user doesn't already exist.
    Returns None otherwise.

    Parameter(s):
        user (dict): A user dictionary containing fields for a new user. May or may not containg: role and/or team.
    """
    user = User(**user_dict)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as ie:
        db.session.rollback()
        return ie.detail
    return user


def edit_user_email(new_email: str, computer_id: int) -> Tuple[str, int]:
    """
    Returns a string with a code whether editing the user succeeded or failed.

    Parameter(s):
        edit (dict): A user dictionary containing the computer_id where the user is and at least one other field to edit.
    """
    # Check if user exists at the computer id
    computer = get_pc_status(computer_id)

    if computer.status < IN_USE_STATUS_CODE:
        return f'No user at computer id {computer_id}', 400

    # Query the usage at the computer
    usage = query_usage(computer.usage_id, esports=True)

    # Get the user with the given id.
    player = query_player(None, usage.player_id)

    if not player:
        return json_response(f"Cannot edit nonexistent user.", 400)

    # Edit player email
    setattr(player, "email", new_email)

    # Commit to database
    try:
        db.session.commit()
    except IntegrityError as ie:
        db.session.rollback()
        return ie.detail

    return json_response(f"Successfully edited user at {computer_id}",
                         200,
                         {'email': player.email})


def create_usage(user_id, computer_id, esports=False):
    """
    Returns a new usage object.

    Parameter(s):
        user_id (int): The id of the user.
        computer_id (int): The id of the computer the user is using.
    """
    if esports:
        usage = EsportUsage(player_id=user_id, computer_id=computer_id)
    else:
        usage = Usage(user_id=user_id, computer_id=computer_id)

    try:
        db.session.add(usage)
        db.session.commit()
    except IntegrityError as ie:
        db.session.rollback()
        return ie.detail
    return usage


def query_usage(usage_id: int, esports=False):
    """
    Returns a new usage with the given usage id if it exists.
    None Otherwise

    Parameter(s):
        usage_id (int): The id of the usage.
    """
    if esports:
        usage = EsportUsage.query.filter_by(usage_id=usage_id).first()
    else:
        usage = Usage.query.filter_by(usage_id=usage_id).first()
    return usage


def add_user_usage(user_usage_dict: dict) -> Tuple[str, int]:
    """
    Returns true with a sucess message if the user usage was added successfully and false with an error message otherwise.

    Parameter(s):
        raw_user (dict): A dictionary containing the fields for a new user.
    """
    # Check if the user exists in the database
    computer_id = user_usage_dict.pop('computer_id')
    user_dict = user_usage_dict

    assert computer_id > 0 and computer_id <= NUM_COMPUTERS
    valid_keys = ('first_name', 'last_name', 'email', 'role', 'team')
    if not all([True if k in valid_keys else False for k in user_dict]):
        return json.dumps({'statusMessage': f"Invalid key in the user dict",
                           'status': 400,
                           'body': None})

    user = query_user(user_dict['email'])

    message = ""

    if not user:
        # Create a new user before creating the new usage log
        user = create_user(user_dict)
        message += f"Successfully created user with email: {user_dict['email']}\n"

    if not user:
        return "Failed to create user.", 400

    # Update new user info data
    user_dict['user_id'] = user.user_id
    user_dict['email_prefix'] = user_dict['email'].split('@')[0]
    user_dict.pop('email')

    # Create new usage log for the user
    usage = create_usage(user.user_id, computer_id)

    if not usage:
        return "Failed to create new usage.", 400

    message += f"Usage created at computer id: {computer_id}"

    return json.dumps({'statusMessage': message, 'status': 200, 'body': {'user_id': user.user_id}})
