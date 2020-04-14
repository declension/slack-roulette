from functools import lru_cache
from logging import getLogger
from typing import Text, Any

import boto3

from chalicelib.config import ConfigStore

logger = getLogger(__name__)
Token = Text


@lru_cache()
def get_ssm():
    ssm = boto3.client("ssm")
    logger.info("Configured SSM in %s", ssm.meta.region_name)
    return ssm


class Error(Exception):
    pass


class SSMConfigStore(ConfigStore):
    """Retrieves arbitrary instance variables from AWS SSM"""

    def __init__(self, prefix: Text) -> None:
        super().__init__()
        if not prefix:
            raise ValueError("Must have a prefix for SSM keys")
        self._prefix = prefix.upper().replace("-", "_").replace(" ", "_")
        logger.info("Using SSM prefix of '%s'", self._prefix)
        self._cache = {}

    def __getattr__(self, name: Text) -> Any:
        """Magical SSM things"""
        param_name = f"{self._prefix}{name.upper()}"
        try:
            return self._cache[param_name]
        except KeyError:
            try:
                self._cache[param_name] = self._get_param(param_name)
                return self._cache[param_name]
            except Exception as e:
                raise Error(f"Couldn't find SSM parameter for '{param_name}'. "
                            f"Is it configured in AWS? ({e!r})")

    def _get_param(self, param_name: Text) -> Text:
        resp = get_ssm().get_parameter(Name=param_name, WithDecryption=True)
        return resp["Parameter"]["Value"]
