# from apiclient import discovery
# from oauth2client.service_account import ServiceAccountCredentials
#
#
#
#
# SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
# KEY_FILE_LOCATION = 'keys.json'
#
# VIEW_ID = 'ga:275676015'
# try:
#     credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
# except FileNotFoundError as e:
#     print(e)
#
#
# analytics = discovery.build('analyticsreporting', 'v4', credentials=credentials)
# try:
#     response = analytics.reports().batchGet(body={
#         'reportRequests': [{
#             'viewId': VIEW_ID,
#             'dateRanges': [{'startDate': 'today', 'endDate': 'today'}],
#             'metrics': [
#                 {"expression": "ga:users"},
#                 # {"expression": "ga:1dayUsers"},
#
#                 # {"expression": "ga:avgSessionDuration"}
#             ], "dimensions": [
#                 {"name": "ga:sessionCount"},
#             ]
#         }]}).execute()
#
#     unique_users_today = response['reports'][0]['data']['totals'][0]['values'][0]
#
#     print(unique_users_today)
# except Exception as e:
#     print(e)
# print(response)
#
