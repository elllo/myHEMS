'''
This is an example of how to send data to Slack webhooks in Python with the
requests module.
Detailed documentation of Slack Incoming Webhooks:
https://api.slack.com/incoming-webhooks

source: https://gist.github.com/devStepsize/b1b795309a217d24566dcc0ad136f784
'''

import json
import requests
import datetime
import time

import credentials

allowable_time_delta = 60  # 60 s equals 1 min

# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
webhook_url = credentials.slack_webhook
slack_data = {'text': "Fenster zu! Es wird ganz schön kalt!"}


def slack_send_message():
    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )
    else: None


with open("/home/pi/myHEMSfiles/slack_cache.txt", "r+") as f:
    try:
        f.seek(0)
        last_notification_time = int(f.read())
        #print("reading has worked", last_notification_time)
    except:
        last_notification_time = 0
        #print("reading hasnot worked")

    current_time = datetime.datetime.now()
    current_time = int(time.mktime(current_time.timetuple()))
    
    if(current_time - last_notification_time >= allowable_time_delta):
        slack_send_message()
        f.seek(0)
        f.write(str(current_time))
        f.truncate()
    else: 
        None
