# from curses.ascii import CR
# import gspread
# import os
# import json
# from dotenv import load_dotenv

# load_dotenv()

# RAW_CREDS = os.environ.get('GOOGLE_CREDS')
# CREDS = json.loads(RAW_CREDS)

# dict_creds = {
#     "type": "service_account",
#     "project_id": "gamer-time-353203",
#     "private_key_id": "273c445cb4fd0449a5faad64191a49798c3806c8",
#     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDPMf67rfqWv1hL\n83wpJ4w+4u7weiO1Q71Bp6njBOM5Z0KFiKkUNSvETvZIEQZoJLsUaAPHFcSnYXSg\nDUMei+FzutXnA4NMDCF1iclYVqzkPADE3tzyDv1XSsqSXW0qNKruBtONAmDoRx+O\nJ1kS/cQyK3khTUy1vE9qGuYT5L/mFyW0XwTwQM1xoy5n2bmf6QhnoVQKY34eW8So\nCYcxCZRoRuuzKLcMU2YaQDXBzd38y0FaLf9KafkCNReiTeND2U0bCLos5sb0vnVw\nD1zyWTeb0rH6qv5J4SS8N9tHsxxqSow2/ffrtVVMN9kyStQ0ioLUhs+oCEjiBXtf\n881gBVo1AgMBAAECggEACNKtcQMF2H0B7swJxbveJEBoIdvloN6nVMAlwxnObj+Y\nLNUGtCpWeIfPQ37cGbu0rrgGLyhdZS5Id9dQvCCDQ3kZijqTUP30P8vUA9u/BYIL\nm1aNLI6YWasA6M4rK6CuBbBLOmY3R7TdomFJEP6259cDk7g1s8h2zkMieIblaBAR\nJO5O8SOVpp2Sd75DrP3pzNj08DV+yjTEJXKDrt/2bSXRCljM81YDzLFyCvbsBZQO\nr+dJFEkMCEj0QQQE4ybowTnbg9zuiN8uKOZOfFpb0robqlX7soLf1BAqVk07K81d\nnOoPx5PXiYFIFWJGgENvPs/lG2khS9eXqJA5pqxNQQKBgQDvmenc23Mjs+5Ve1Qc\nKwX9p5H2wnZlLqFnHEYghDtWT9I5DF9JifP3S4Woj+b8K8tpJLZx0ZILMPecDjia\n45hBS/iOGHn1lQUt59pDQ07gHZPShxrRm2X4cMYR7bp/rL2Z6O8WoWzeVJmqo5CD\ncXtJGa7hN6VedShHeixdYH8sdQKBgQDdYErtAsxxpthFY/snVCFqZwLLOqGUV8T5\nVR9TvhtK2+nkAtTGdBa5HS7A/FV3P0bGTUYcYia4YEv+5SA7CUnKyBqtID2KI7BJ\nbZu8TywVNY36ctawrxIh0fJPyYKxmzd13kRjPPiIdMeFkp3MKQxKDvLQ8TOhzJ6B\nDXDSu86+wQKBgQDLt8e5uvSYxKG+GJAZKxN66gEXF5xmx1EARG/zsbpp1pBdZQGX\nmy3Nc27/NOsmOW5HxalB+Pf9f/LnwseqGh0YV6nL10/K2JuAvoM7cX0c3MkU1T6e\nPUxkAi7Gi6Robcz/kafHTBUurCvDhDKZL+Gs86NXZmK6f05yB5S1CBjZCQKBgQCX\nAvLZjwkrlib93uAayfcpgC+Vtt82NFE3zGtcUtiHTlDUq2G+Jr7BdDjKiNc8Szva\nVig3gHTtXTM6I87CtulRnQMlilKwgvvkexK7eD6YETpS2De/uw1haLgk2U+AHGPO\n0dpQ3+yiGRdp9MQT2wR5GI1nHsKb4ttVKXgHKPo1gQKBgQC6BiK/zCkglW/kUAZ0\ngzm6ULNSqxaeqGocZnl6de6GXK5iBswYj2URmQ0Os5cEr7OSJPH2NJ8Phaq1MAzD\nLmVPBMiRQ3gdTUwwmeQP0xqUEQuhlNtjjOg8a/brJHFnYv70a5FAPVgoOdYqYrVx\nJPzgonIIAaR1jdVzKFrNaUVboQ==\n-----END PRIVATE KEY-----\n",
#     "client_email": "gtime2-0@gamer-time-353203.iam.gserviceaccount.com",
#     "client_id": "104252684902505440753",
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gtime2-0%40gamer-time-353203.iam.gserviceaccount.com"
# }

# # for k in dict_creds:
# #     if dict_creds[k] != CREDS[k]:
# #         d1 = dict_creds[k]
# #         d2 = CREDS[k]
# #         for i in range(len(d2)):
# #             if d1[i] != d2[i]:
# #                 print(i)
# #         print(d1[675:700])
# #         print(d2[675:700])

# # Initial gspread instance
# gc = gspread.service_account_from_dict(CREDS)
# CURRENT_SHEET_ID = "1AErY7nT-7nYShnLenN3KjRMnst1xh_EIsv-76ybDfqI"

# sheet = gc.open_by_key(CURRENT_SHEET_ID)

# sh = gc.open("Gamer Time Test Sheet")

# # print(sh.sheet1.get('A1'))
