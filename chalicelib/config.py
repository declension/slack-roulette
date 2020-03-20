import os
from typing import Any


class ConfigStore:
    pass


class EnvConfigStore(ConfigStore):
    def __getattr__(self, name: str) -> Any:
        return os.environ[name.upper()]
