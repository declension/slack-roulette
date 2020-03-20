from logging import basicConfig, INFO, getLogger

NICE_LOG_FORMAT = "%(levelname)-7s [%(name)-35s] %(message)s"
getLogger().handlers.clear()
basicConfig(level=INFO, format=NICE_LOG_FORMAT)
