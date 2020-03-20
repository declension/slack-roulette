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

    def __init__(self) -> None:
        super().__init__()
        self._cache = {}

    def __getattr__(self, name: Text) -> Any:
        """Magical SSM things"""
        param_name = name.upper()
        try:
            return self._cache[param_name]
        except KeyError:
            try:
                param = get_ssm().get_parameter(Name=param_name, WithDecryption=True)

                value = param["Parameter"]["Value"]
                self._cache[param_name] = value
                return self._cache[param_name]
            except Exception as e:
                raise Error(f"Couldn't find SSM parameter for '{param_name}'. "
                            f"Is it configured in AWS? ({e!r})")
