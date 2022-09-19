import googleapiclient
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'keys.json'
VIEW_ID = '332621189'
try:
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
except FileNotFoundError as e:
    print(e)

# Build the service object.
analytics = discovery.build('analyticsreporting', 'v4', credentials=credentials)
try:
    response = analytics.reports().batchGet(body={
        'reportRequests': [{
            'viewId': VIEW_ID,
            'dateRanges': [{'startDate': '2022-09-18', 'endDate': '2022-09-19'}],
            'metrics': [
                {"expression": "ga:pageviews"},
                {"expression": "ga:avgSessionDuration"}
            ], "dimensions": [
                {"name": "ga:deviceCategory"}
            ]
        }]}).execute()
except Exception as e:
    print(e)

