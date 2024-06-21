REDIS_URL = "redis://biome_redis.biome:6379"

# Queues to listen on
QUEUES = ["high", "default", "low"]

DICT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",  # Default is stderr
        },
        "debug_rotating_file_handler": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/worker.log",
            "mode": "a",
            "maxBytes": 1048576,
            "backupCount": 10,
        },
    },
    "loggers": {
        "root": {  # root logger
            "handlers": ["default", "debug_rotating_file_handler"],
            "level": "INFO",
            "propagate": False,
        },
    },
}