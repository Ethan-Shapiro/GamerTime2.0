from datetime import date, datetime, timezone, timedelta
import zoneinfo
import gspread
import json
import os
from datetime import date, datetime
from gspread_formatting import *
import base64
import sqlalchemy

db_user = os.environ["DB_USER"]  # e.g. 'my-database-user'
db_pass = os.environ["DB_PASS"]  # e.g. 'my-database-password'
db_name = os.environ["DB_NAME"]  # e.g. 'my-database'
# e.g. '/cloudsql/project:region:instance'
unix_socket_path = os.environ["INSTANCE_UNIX_SOCKET"]

pool = sqlalchemy.create_engine(
    # Equivalent URL:
    # postgresql+pg8000://<db_user>:<db_pass>@/<db_name>
    #                         ?unix_sock=<INSTANCE_UNIX_SOCKET>/.s.PGSQL.5432
    # Note: Some drivers require the `unix_sock` query parameter to use a different key.
    # For example, 'psycopg2' uses the path set to `host` in order to connect successfully.
    sqlalchemy.engine.url.URL.create(
        drivername="postgresql+pg8000",
        username=db_user,
        password=db_pass,
        database=db_name,
        query={"unix_sock": "{}/.s.PGSQL.5432".format(unix_socket_path)},
    ),
)

# Get the credentials needed from the environment
RAW_CREDS = os.environ.get('GOOGLE_CREDS')
CREDS = json.loads(RAW_CREDS)

# Initial gspread instance
gsheet = gspread.service_account_from_dict(CREDS)
pacifictz = zoneinfo.ZoneInfo("US/Pacific")


def write_to_sheet(event, context):

    print("Started nightly update")
    print(datetime.utcnow())
    print(event)
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)
    sheet_id = pubsub_message.strip()
    openrec_successful = save_openrec_usages()


def update_sheet(worksheet, usages, dse_roster):
    """
    Updates the google worksheet with the usages provided
    """
    # Get all values from dse_roster
    dse_data = dse_roster.get_all_values()

    # Check if name or email is in dse_data for the team and return their status
    def get_dse_status(name, email):
        # Iterate through rows and check each item
        name_i = 1
        email_i = 3
        status_i = 4
        for row in dse_data:
            if row[name_i].lower() == name.lower() or row[email_i].lower() == email.lower():
                return row[status_i]
        return "Incomplete"

    start_cell = 'A1'
    data = [('First', 'Last', 'Email', 'Start_time',
             'End_time', 'Team', 'Computer_id', "DSE_status")]

    user_ids = set([usage.user_id for usage in usages])
    users = query_users(user_ids)

    end_cell_num = 1
    for i in range(len(usages)):
        start_time = usages[i].start_timestamp.strftime("%I:%M %p")
        end_time = usages[i].end_timestamp.strftime("%I:%M %p")
        dse_status = get_dse_status(users[i].first_name, users[i].email)
        data.append([users[i].first_name, users[i].last_name, users[i].email,
                    start_time, end_time, users[i].team, usages[i].computer_id, dse_status])
        end_cell_num += 1
    end_cell = f'H{end_cell_num}'

    cells = ':'.join((start_cell, end_cell))

    worksheet.update(cells, data)
    return cells


def create_sheet(sheet, title: str, rows: int, cols: int):
    """
    Creates a new worksheet with the default format in the specified google sheet.
    """
    if int(rows) <= 0:
        rows = 1
    if int(cols) <= 0:
        cols = 1

    try:
        new_sheet = sheet.add_worksheet(title=title, rows=rows, cols=cols)
    except Exception as e:  # Probably already created.
        if 'already exists' in e.args[0]['message']:
            new_sheet = sheet.worksheet(title=title)
    return new_sheet


def format_openrec_sheet(sheet, cells: str):
    heading_format = CellFormat(
        backgroundColor=Color(0.9, 0.9, 1),
        textFormat=TextFormat(bold=True, fontSize=14),
        horizontalAlignment='CENTER'
    )
    format_cell_range(sheet, 'A1:H1', heading_format)
    rules = get_conditional_format_rules(sheet)
    rules.save()
    return True


def save_openrec_usages() -> bool:
    OPEN_REC_SHEET_ID = '1L79q6FFIpxjgtnsp0ugw7Hvx9jrOHikjhxlfO-rOg20'
    # Load the OpenRec Google Sheet
    openrec_sheet = gsheet.open_by_key(OPEN_REC_SHEET_ID)

    # Get the OpenRec Usages
    usages, date = get_openrec_days_usages()
    if len(usages) == 0:
        return True

    month_day_str = f'{str(date.month)}/{str(date.day)}'

    # Create a new sheet
    new_sheet = create_sheet(openrec_sheet, title=month_day_str, rows=len(
        usages), cols=len(usages[0].get_columns())-1)

    # Add OpenRecUsages to the sheet
    cells = write_openrec_usages(new_sheet, usages)

    # Apply formatting
    format_openrec_sheet(new_sheet, cells)

    return True


def convert_to_pacific(timestamp: datetime) -> datetime:
    PST_UTC_OFFSET = timedelta(hours=-7)
    return (timestamp + PST_UTC_OFFSET).astimezone(pacifictz)


def write_openrec_usages(worksheet, usages: list):
    start_cell = 'A1'
    data = [('Usage_id', 'Computer_id', 'Start_time',
             'End_time')]

    end_cell_num = 1
    for i in range(len(usages)):
        start_time = convert_to_pacific(
            usages[i].start_timestamp).strftime("%I:%M %p")
        end_time = convert_to_pacific(
            usages[i].end_timestamp).strftime("%I:%M %p")
        data.append([usages[i].id, usages[i].computer_id,
                    start_time, end_time])
        end_cell_num += 1
    end_cell = f'D{end_cell_num}'

    cells = ':'.join((start_cell, end_cell))

    worksheet.update(cells, data)
    return cells
