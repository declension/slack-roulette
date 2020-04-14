from typing import Text, Dict
from urllib.parse import parse_qs

from slack.errors import SlackApiError

from chalicelib.aws import SSMConfigStore
from chalicelib.chalice import SecretiveChalice
from chalicelib.slack import LazySlackClient, BULLET, response_for_members

APP_NAME = "slack-roulette"
config = SSMConfigStore(prefix="SLACK_ROULETTE_")
slack_client = LazySlackClient(config)
app = SecretiveChalice(app_name=APP_NAME, slack_client=slack_client)


@app.route("/slack/commands", methods=["POST"],
           content_types=['application/x-www-form-urlencoded'])
def roulette():
    data = parse_qs(app.current_request.raw_body.decode())
    app.log.info("Got %s command with data: %s", data.get("command"), data)
    try:
        channel_id = data["channel_id"][0]
        channel_type = data.get("channel_name")[0]
    except (KeyError, IndexError) as e:
        app.log.error(f"Couldn't get channel details from {data} ({e!r}")
        return simple_message("Couldn't get channel details from Slack")
    if channel_type in {"directmessage"}:
        app.log.info("Reminding @%s this won't work...", data.get("user_name"))
        return simple_message("Can't do this in conversations! "
                              "Try a channel...")
    try:
        client = app.slack_client
        app.log.info("Getting members of channel %s", channel_id)
        resp = client.conversations_members(channel=channel_id).validate()
    except SlackApiError as e:
        app.log.error("Couldn't get conversation members from Slack API (%r)",
                      e)
        return simple_message(":disappointed: "
                              "Got stuck getting channel members")
    app.log.info("Got API response: %s", resp)
    member_ids = resp.get("members")
    body = response_for_members(member_ids)
    return {
        "response_type": "in_channel",
        "text": f":game_die: How about chats between:\n {BULLET} {body}",
        "delete_original": "true"
    }


def simple_message(text: Text) -> Dict[Text, Text]:
    return {"response_type": "in_channel", "text": text}
