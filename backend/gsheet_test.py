import gspread
import json
import os
from dotenv import load_dotenv

load_dotenv()

RAW_CREDS = os.environ.get('GOOGLE_CREDS')
CREDS = json.loads(RAW_CREDS)

gc = gspread.service_account_from_dict(CREDS)
CURRENT_SHEET_ID = "1AErY7nT-7nYShnLenN3KjRMnst1xh_EIsv-76ybDfqI"
sh = gc.open_by_key(CURRENT_SHEET_ID)

print(sh.sheet1.get('A1'))
