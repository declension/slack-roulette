import asyncio
from html import escape, unescape
from logging import getLogger
from typing import Text, Any, Optional

from slack import WebClient
from slack.web.base_client import BaseClient

from chalicelib.config import ConfigStore

Token = Text

logger = getLogger(__name__)


def sanitise(s: Text):
    return escape(unescape(s), False)


class LazySlackClient(WebClient):
    """Lazily gets the token via a ConfigStore"""
    _INSTANCE = None

    def __new__(cls, *args, **kwargs) -> Any:
        if not cls._INSTANCE:
            cls._INSTANCE = super().__new__(cls)
        return cls._INSTANCE

    def __init__(self,
                 config: ConfigStore,
                 base_url=BaseClient.BASE_URL,
                 timeout=30,
                 loop: Optional[asyncio.AbstractEventLoop] = None,
                 ssl=None,
                 proxy=None,
                 run_async=False,
                 session=None,
                 headers: Optional[dict] = None,
                 ):
        self.base_url = base_url
        self.timeout = timeout
        self.ssl = ssl
        self.proxy = proxy
        self.run_async = run_async
        self.session = session
        self.headers = headers or {}
        self._logger = getLogger(__name__)
        self._event_loop = loop

        # Overriden / extra
        self._token = None
        self.config = config
        self._logger.info("Created new %s (to %s)", type(self).__name__,
                          self.base_url)

    @property
    def token(self) -> Token:
        """Lazy, cached token access"""
        if not self._token:
            self._token = self.config.slack_api_token
        return self._token
