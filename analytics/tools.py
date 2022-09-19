from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials


def get_unique_users_today():
    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
    KEY_FILE_LOCATION = 'keys.json'
    VIEW_ID = 'ga:275676015'
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
        analytics = discovery.build('analyticsreporting', 'v4', credentials=credentials)
        response = analytics.reports().batchGet(body={
            'reportRequests': [{
                'viewId': VIEW_ID,
                'dateRanges': [{'startDate': 'today', 'endDate': 'today'}],
                'metrics': [
                    {"expression": "ga:users"},
                ], "dimensions": [
                    {"name": "ga:sessionCount"},
                ]
            }]}).execute()

        unique_users_today = response['reports'][0]['data']['totals'][0]['values'][0]
        return unique_users_today
    except FileNotFoundError as e:
        print(e)
