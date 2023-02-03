from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from flask import current_app as app
from application import apscheduler
from . import db
from datetime import datetime, timezone, timedelta
import zoneinfo
import re
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True

# set our timezone to UTC so all datetime objects inserted are consistent


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


# GLOBAL VAIRABLES
NUM_COMPUTERS = 26
IN_USE_STATUS_CODE = 1
DISABLED_STATUS_CODE = -1
IDLE_STATUS_CODE = 0

# Intialize timezone
pacifictz = zoneinfo.ZoneInfo("US/Pacific")


class User(db.Model):
    """
    Outline for the User model in PSQL 
    """
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String, nullable=False)
    permissions = db.Column('permissons', db.String(16))
    role = db.Column('role', db.String(7), nullable=False)
    team = db.Column('team', db.String(5), nullable=False)
    salt = db.Column('salt', db.String(16))
    password = db.Column('password', db.String(64))

    def __init__(self, email, permissions, role, team, salt, password):
        self.email = email
        self.permissions = permissions
        self.role = role
        self.team = team
        self.salt = salt
        self.password = password

    def get_id(self):
        return (self.id)

    def has_permissions(self, perms):
        return perms in self.permissions


class ComputerStatus(db.Model):
    """
    Outline for the Computer Status model in PSQL
    """
    id = db.Column('id', db.Integer, primary_key=True)
    status = db.Column('status', db.Integer, nullable=False)
    start_timestamp = db.Column(
        'start_timestamp', db.DateTime)
    email = db.Column('email', db.String)

    def __init__(self, status, start_timestamp, email):
        self.status = status
        self.start_timestamp = start_timestamp
        self.email = email


class Usage(db.Model):
    """
    Outline for the Usage model in PSQL
    """
    id = db.Column('id', db.Integer, primary_key=True)
    player_id = db.Column('player_id', db.Integer,
                          db.ForeignKey('player.id'), nullable=False)
    computer_id = db.Column('computer_id', db.Integer,
                            db.ForeignKey('computer_status.id'), nullable=False)
    start_timestamp = db.Column(
        'start_timestamp', db.DateTime, server_default=utcnow())
    end_timestamp = db.Column('end_timestamp', db.DateTime)

    def __init__(self, player_id, computer_id):
        self.player_id = player_id
        self.computer_id = computer_id

    def get_columns(self):
        return {'id', 'player_id', 'computer_id', 'start_timestamp', 'end_timestamp'}


class Player(db.Model):
    """
    Outline for the Player model in PSQL
    """
    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(50), nullable=False)
    last_name = db.Column('last_name', db.String(50), nullable=False)
    email = db.Column('email', db.String, nullable=False)
    role = db.Column('role', db.String(7), nullable=False)
    team = db.Column('team', db.String(5), nullable=False)

    def __init__(self, first_name, last_name, email, role, team):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role
        self.team = team


class Queue(db.Model):
    """
    Outline for the Queue model in PSQL
    """
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String)


def valid_ucsd_email(email: str) -> bool:
    """
    Helper function that takes in an email string
    and returns True if the email string is a valid ucsd email.

    Args:
        email (str): An email string to check

    Returns:
        bool: True if the email string is a valid ucsd email
    """
    # ucsd emails must start with only alphanumeric characters
    # and must end in '@ucsd.edu'
    pattern = re.compile('^[A-Za-z0-9]*@ucsd\.edu$')
    return re.fullmatch(pattern, email)


def get_esports_conflicting_hrs() -> dict:
    """
    Returns a dict of the pc number and the hours that are conflicting that day.
    Returns None if no hours are conflicting

    Returns:
        dict: A dictioanry of pairs of pc numbers and a range of conflicting hours.
    """
    # TODO use google api to access sheet containing conflicts

    # TODO return the conflicitng times in military time

    # TESTING data
    return {}


def get_pc_status(computer_id: int) -> ComputerStatus:
    """
    Returns the ComputerStatus object of the given computer id.
    None if the computer id is invalid.

    Args:
        computer_id (int): The computer id to get the status of

    Returns:
        ComputerStatus: An object containing attributes about the computer's status
    """
    computer = ComputerStatus.query.filter_by(id=computer_id).first()
    return computer


def get_computer_availability() -> list[int]:
    """
    Returns a list of computer id's in the order which computers
    are open followed by the computers being used the longest.

    Returns:
        list[int]: A list of computer ids
    """
    statuses = ComputerStatus.query.order_by(
        ComputerStatus.start_timestamp.desc(), ComputerStatus.id).all()
    return [c.id for c in statuses]


def set_pc_in_use(computer_id: int, email=None) -> tuple[bool, dict]:
    """
    Attempts to change the status of the computer id to in use.
    Returns whether the query succeeded and a message.

    Args:
        computer_id (int): The computer ID to set into use
        email (string, optional): The email address of the user if provided. Defaults to None.

    Returns:
        Tuple[bool, dict]: A success bool and dictionary containing a message and potentially data.
    """
    # Get the current computer from db
    computer = get_pc_status(computer_id)

    if computer.status == DISABLED_STATUS_CODE:
        return False, {'message': f"Computer at {computer_id} is disabled."}

    if computer.status >= IN_USE_STATUS_CODE:
        return True, {'message': f"A different use was started here!", "id": 1,
                      "start_timestamp": str(computer.start_timestamp.timestamp()),
                      "status": computer.status}

    # If there is an email provided, we are in esports and don't have a timer
    if email:
        # Query for the users email
        player = query_player(email)

        if player == None:
            return False, {'message': f"Player with email {email} doesn't exist."}

        # Create new usage
        new_usage = create_usage(player.id, computer_id)

    else:
        # query for open rec user id
        open_rec_user = query_player('openrec@ucsd.edu')

        # Create new usage
        new_usage = create_usage(open_rec_user.id, computer_id)

    # Change timezone to utc
    start_timestamp_seconds = datetime.timestamp(new_usage.start_timestamp.replace(
        tzinfo=timezone.utc))

    # Change the current status of the computer in Postgres
    worked = change_pc_status(
        computer, new_usage.id, new_usage.start_timestamp, email)

    if email:
        body = {'id': computer_id, 'status': new_usage.id,
                'email': email}
    else:
        body = {'id': computer_id, 'status': new_usage.id,
                'start_timestamp': start_timestamp_seconds}

    if not worked:
        return False,
    return worked, {'message': "Success!"} | body


def change_pc_status(computer: ComputerStatus, status: int, start_timestamp=None, email=None) -> bool:
    """
    Changes the status, timestamp, and email of the given computer.
    Returns True if the change as successful.

    Args:
        computer (ComputerStatus): The computer status to update
        status (int): The new status.
        start_timestamp (datetime, optional): The start datetime. Defaults to None.
        email (str, optional): The email to change the computer status to. Defaults to None.

    Returns:
        bool: True when the status change succeeded.
    """
    computer.status = status
    computer.start_timestamp = start_timestamp
    computer.email = email
    try:
        db.session.commit()
    except IntegrityError as ie:
        db.session.rollback()
        return False
    return True


def end_usage_change_status(usage_id: int, computer_id: int) -> bool:
    """
    End the current computer usage and also changes the status of the pc
    to be the IDLE status.

    Parameter(s):
        usage_id (int): The usage id to end.
        computer_id (int): The id of the computer to change status.
        esports (bool): Whether the session to end was esports (default False).
    """
    # Query for the usage and the computer
    usage = query_usage(usage_id)
    computer = get_pc_status(computer_id)

    # Update the parameters
    if usage == None:
        return False

    # Set the attributes
    setattr(usage, 'end_timestamp', datetime.utcnow())
    setattr(computer, 'status', IDLE_STATUS_CODE)
    setattr(computer, 'start_timestamp', None)
    setattr(computer, 'email', None)

    try:
        db.session.commit()
        return True
    except IntegrityError as ie:
        db.session.rollback()
        return False


def end_pc_use(usage_id: int, computer_id: int, esports=False, scheduled=False) -> tuple[bool, dict]:
    """
    Attempts to end the given computer usage by changing computer with given computer id
    to the IDLE status code. If the PC is being used by a new user, this returns a dictionary
    containing the new user data.

    Args:
        usage_id (int): ID of the usage from the frontend
        computer_id (int): A computer ID to change status
        esports (bool, optional): Whether the usage is an esports usage. Defaults to False.
        scheduled (bool, optional): Whether the function call was scheduled . Defaults to False.

    Returns:
        tuple[bool, dict]: _description_
    """
    # Get the current computer from db
    computer = get_pc_status(computer_id)

    if esports:
        body = {'id': computer_id,
                'status': 0,
                'email': '',
                "message": ''}
    else:
        body = {'id': computer_id,
                'status': 0,
                'start_timestamp': '',
                "message": ""}

    if computer.status == DISABLED_STATUS_CODE:
        body['message'] = 'Computer is disabled.'
        body['status'] = DISABLED_STATUS_CODE
        return False, body

    # If the usage_id passed by the front-end
    # doesn't match the one stored in the server,
    # that means the front-end is unsynced and we can send the updated data
    if computer.status != usage_id:
        body['status'] = computer.status
        body['message'] = f'Old computer use already ended at computer {computer_id}.'
        if esports:
            body['email'] = computer.email
        else:
            body['start_timestamp'] = computer.start_timestamp
        return False, body

    # We must execute the scheduled end
    #  within the context of the applicaiton
    app = apscheduler.app
    with app.app_context():
        # attempt to end usage on database
        ended_usage = end_usage_change_status(usage_id, computer_id)
        if not ended_usage:
            body['message'] = f'Failed to end session at: {computer_id}.'
            return False, body

        if not scheduled:
            try:
                # Need to remove scheduled end or else we will error
                job_id = f'auto_end_{usage_id}'
                apscheduler.remove_job(job_id)
                print("Successfully ended scheduled session")
            except:
                print("Couldn't find scheduled session end")
        body['message'] = f'Successfully ended session at: {computer_id}.'
        return True, body


# @cache.memoize(timeout=30)
def get_db_pc_usages(esports=False) -> list[dict]:
    """
    Returns a list of usages as dictionaries that are in use.
    When Esports is true, we add the start timestamp to the dictionary.

    Args:
        esports (bool, optional): Whether we are accessing esports or not. Defaults to False.

    Returns:
        list[dict]: List of dictionaries containing attributes from Usages.
    """
    if esports:
        usages = ComputerStatus.query.filter(ComputerStatus.status != 0).with_entities(
            ComputerStatus.id, ComputerStatus.status, ComputerStatus.email
        ).order_by(ComputerStatus.id).all()
    else:
        usages = ComputerStatus.query.filter(ComputerStatus.status != 0).with_entities(
            ComputerStatus.id, ComputerStatus.status, ComputerStatus.start_timestamp
        ).order_by(ComputerStatus.id).all()
    usages = [dict(x) for x in usages]
    for usage in usages:
        usage['start_timestamp'] = str(usage['start_timestamp'].timestamp())
        print(usage)
    return usages


def get_openrec_days_usages() -> tuple[list[Usage], datetime]:
    today = datetime.utcnow() - timedelta(hours=24)
    usages = Usage.query.filter(
        Usage.start_timestamp >= today, Usage.player_id == 2).all()
    return usages, today


def get_days_usages() -> tuple[list[Usage], datetime]:
    """
    Returns the usages from today as a list of Usages and today's date.
    """
    today = datetime.utcnow() - timedelta(hours=24)
    usages = Usage.query.filter(Usage.start_timestamp >= today).all()
    return usages, today


def query_users(user_ids: set) -> list[User]:
    """
    Returns the information of the given user ids. None if the user doesn't exist.
    """
    return User.query.filter(User.id.in_(user_ids)).all()


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
        player = Player.query.filter_by(id=player_id).first()
    else:
        return None
    return player


def create_player(player_dict: dict) -> User:
    """
    Returns a newly created user with the given values and adds that user to the database if that user doesn't already exist.
    Returns None otherwise.

    Parameter(s):
        user (dict): A user dictionary containing fields for a new user. May or may not containg: role and/or team.
    """
    player = Player(**player_dict)

    try:
        db.session.add(player)
        db.session.commit()
    except IntegrityError as ie:
        db.session.rollback()
        return False, ie.detail
    return True, player


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


def create_usage(user_id: int, computer_id: int) -> Usage:
    """
    Returns a new usage object.

    Parameter(s):
        user_id (int): The id of the user.
        computer_id (int): The id of the computer the user is using.
    """
    usage = Usage(player_id=user_id, computer_id=computer_id)

    try:
        db.session.add(usage)
        db.session.commit()
    except IntegrityError as ie:
        db.session.rollback()
        return ie.detail
    return usage


def query_usage(usage_id: int) -> Usage:
    """
    Returns a new usage with the given usage id if it exists.
    None Otherwise

    Parameter(s):
        usage_id (int): The id of the usage.
    """
    usage = Usage.query.filter_by(id=usage_id).first()
    return usage


def recreate_computer_statuses() -> bool:
    # can't drop if the table doesn't exist yet
    inspector = inspect(db.engine)
    try:
        if inspector.has_table('computer_status') and db.session.query(ComputerStatus).count() != 0:
            if db.session.query(ComputerStatus).count() != 26:
                print("incorrect number of rows")
                return False
        else:
            for i in range(26):
                new_comp_stat = ComputerStatus(0, None, None)
                db.session.add(new_comp_stat)
            db.session.commit()
    except Exception as e:
        print(e)
        return False
    print(db.session.query(ComputerStatus).count())
    return True


def reset_computer_statuses_table() -> bool:
    try:
        computer_statuses = ComputerStatus.query.all()
        for comp_stat in computer_statuses:
            # end the computer usage if it is being used
            if comp_stat.status != 0:
                end_usage_change_status(comp_stat.status, comp_stat.id)
        db.session.commit()
    except:
        return False
    return True


def drop_computer_table():
    Usage.__table__.drop(db.engine)
    ComputerStatus.__table__.drop(db.engine)


def get_queue() -> list[dict]:
    queue_items = Queue.query.order_by(Queue.id).all()
    return [{'id': q.id, 'name': q.name} for q in queue_items]


def add_to_queue(first, last):
    if not first or not last:
        return False, {'message': 'No names to add.'}
    combined_name = first + ' ' + last[0] + '.'
    try:
        new_queue_item = Queue(name=combined_name)
        db.session.add(new_queue_item)
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True, {'id': new_queue_item.id, 'name': new_queue_item.name}


def remove_from_queue(queue_id) -> bool:
    try:
        Queue.query.filter_by(id=queue_id).delete()
        db.session.commit()
    except:
        return False
    return True


# Queue.__table__.drop(db.engine)
# drop_computer_table()
# print(ComputerStatus.query.all())
# print(User.query.all())
