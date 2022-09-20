from datetime import date, datetime, timezone, timedelta
import zoneinfo
import gspread
import json
import os
from datetime import date, datetime
from .models import get_days_usages, query_users, get_openrec_days_usages
from . import apscheduler
from gspread_formatting import *


# Get the credentials needed from the environment
RAW_CREDS = os.environ.get('GOOGLE_CREDS')
CREDS = json.loads(RAW_CREDS)

# Initial gspread instance
gsheet = gspread.service_account_from_dict(CREDS)
CURRENT_SHEET_ID = "1AErY7nT-7nYShnLenN3KjRMnst1xh_EIsv-76ybDfqI"
pacifictz = zoneinfo.ZoneInfo("US/Pacific")


# @apscheduler.task('interval', id='testing_apscheduler', seconds=10)
def testing_print():
    print("Apscheduler worked!")


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


def format_sheet(worksheet, cells: str):
    """
    Formats the given sheet with the defined formatting rules
    """
    heading_format = CellFormat(
        backgroundColor=Color(0.9, 0.9, 1),
        textFormat=TextFormat(bold=True, fontSize=14),
        horizontalAlignment='CENTER'
    )

    cells = cells.replace('A', 'H')
    dse_incomplete_format = ConditionalFormatRule(
        ranges=[GridRange.from_a1_range(cells, worksheet)],
        booleanRule=BooleanRule(
            condition=BooleanCondition('TEXT_CONTAINS', values=['Incomplete']),
            format=CellFormat(backgroundColor=Color(1, 0, 0, 0.6)))
    )

    dse_pending_format = ConditionalFormatRule(
        ranges=[GridRange.from_a1_range(cells, worksheet)],
        booleanRule=BooleanRule(
            condition=BooleanCondition(
                'TEXT_CONTAINS', values=['Pending Approval']),
            format=CellFormat(backgroundColor=Color(1, 1, 0, 0.6)))
    )

    dse_missing_format = ConditionalFormatRule(
        ranges=[GridRange.from_a1_range(cells, worksheet)],
        booleanRule=BooleanRule(
            condition=BooleanCondition(
                'TEXT_CONTAINS', values=['Missing Requirements']),
            format=CellFormat(backgroundColor=Color(1, .27, 0, 0.6)))
    )

    dse_active_format = ConditionalFormatRule(
        ranges=[GridRange.from_a1_range(cells, worksheet)],
        booleanRule=BooleanRule(
            condition=BooleanCondition(
                'TEXT_CONTAINS', values=['Approved-Active']),
            format=CellFormat(backgroundColor=Color(0, 1, 0, 0.6)))
    )

    format_cell_range(worksheet, 'A1:H1', heading_format)
    rules = get_conditional_format_rules(worksheet)
    rules.append(dse_incomplete_format)
    rules.append(dse_pending_format)
    rules.append(dse_missing_format)
    rules.append(dse_active_format)
    rules.save()


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


# save_openrec_usages()


def save_esports_usages():
    # Get the days usage and date from database
    usages, date = get_days_usages()

    items_in_usage = 7

    # If we have no used computers today, do nothing.
    if len(usages) <= 0:
        return

    month_day_str = f'{str(date.month)}/{str(date.day)}'

    # Access the google sheet
    sheet = gsheet.open_by_key(CURRENT_SHEET_ID)

    # Access DSE roster worksheet
    dse_sheet = sheet.worksheet(title="DSE Roster")

    # Add a new worksheet for the day
    worksheet = create_sheet(sheet, month_day_str,
                             len(usages), items_in_usage)

    # Add usages to sheet
    cells = update_sheet(worksheet, usages, dse_sheet)

    # Format cells
    format_sheet(worksheet, cells)


# @apscheduler.task('interval', id='nightly_update', hours=24, start_date='2022-09-6 22:07:00', misfire_grace_time=900)
# @apscheduler.task('interval', id='nightly_gsheet_update', seconds=30, misfire_grace_time=900)
def nightly_update():
    """
    Creates and updates the google sheet every night at 11:50pm for the entries from the last day.
    """
    app = apscheduler.app
    with app.app_context():
        print("Started nightly update")
        print(datetime.utcnow())
        openrec_successful = save_openrec_usages()

        print("Successfully updated the computer stuff for the night.")
        return "Completed"
