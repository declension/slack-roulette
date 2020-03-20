from chalice.app import Chalice
from slack import WebClient

from chalicelib import NICE_LOG_FORMAT


class SecretiveChalice(Chalice):
    """Like normal, but:
        * Takes custom dependencies
        * Nicer log format"""
    FORMAT_STRING = NICE_LOG_FORMAT

    def __init__(self, app_name,
                 slack_client: WebClient,
                 debug=True, configure_logs=True, env=None):
        super().__init__(app_name, debug=debug, configure_logs=configure_logs,
                         env=env)
        self.slack_client = slack_client
        self.log.info("Started up %s", type(self).__name__)
