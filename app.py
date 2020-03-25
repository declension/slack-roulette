from typing import Iterable
from urllib.parse import parse_qs

from chalicelib.aws import SSMConfigStore
from chalicelib.chalice import SecretiveChalice
from chalicelib.roulette import choose_pairs, UserId
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
        return {"response_type": "in_channel",
                "text": "Couldn't get channel ID for Slack"
                }
    try:
        channel_type = data.get("channel_name")[0]
    except (KeyError, IndexError) as e:
        app.log.error(f"Couldn't get channel name from {data} ({e!r}")
        return {}
    if channel_type in {"directmessage"}:
        return {"response_type": "in_channel",
                "text": "Can't do this in conversations! Try in a channel.."
                }
    resp = slack_client.conversations_members(channel=channel_id).validate()
    app.log.info("Got API response: %s", resp)
    member_ids = resp.get("members")
    body = response_for_members(member_ids)
    return {
        "response_type": "in_channel",
        "text": f":game_die: {APP_NAME} users:\n * {body}",
        "delete_original": "true"
    }


def response_for_members(member_ids: Iterable[UserId]):
    combos = choose_pairs(member_ids)
    return '\n * '.join(f"<@{mid1}> <-> <@{mid2}>" for mid1, mid2 in combos)

