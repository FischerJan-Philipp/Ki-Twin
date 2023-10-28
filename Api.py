import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask  import Flask
from slackeventsapi import SlackEventAdapter

from slack.errors import SlackApiError

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['signing_secret'], '/slack/events', app)

client = slack.WebClient(token=os.environ['slack_token_bot'])

client.chat_postMessage(channel='#bot', text="Was geht")
BOT_ID = client.api_call("auth.test")['user_id']


@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')


    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=text)



if __name__ == "__main__":
    app.run(debug=True)


