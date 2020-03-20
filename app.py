from urllib.parse import parse_qs

from chalicelib.aws import SSMConfigStore
from chalicelib.chalice import SecretiveChalice
from chalicelib.slack import LazySlackClient

APP_NAME = "slack-roulette"
config = SSMConfigStore()
slack_client = LazySlackClient(config)
app = SecretiveChalice(app_name=APP_NAME, slack_client=slack_client)


@app.route("/slack/commands", methods=["POST"],
           content_types=['application/x-www-form-urlencoded'])
def commands():
    data = parse_qs(app.current_request.raw_body.decode())
    app.log.info("Got command with data: %s", data)
    try:
        channel_id = data["channel_id"][0]
    except (KeyError, IndexError) as e:
        app.log.error(f"Couldn't get channel ID from {data} ({e!r}")
        return {}
    resp = slack_client.conversations_members(channel=channel_id).validate()
    app.log.info("Got API response: %s", resp)
    member_ids = resp.get("members")
    body = '\n * '.join(f"<@{id}>" for id in member_ids)
    return {
        "response_type": "in_channel",
        "text": f":game_die: {APP_NAME} users:\n * {body}",
        "delete_original": "true"
    }
