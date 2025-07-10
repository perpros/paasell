import logging
import sys

# Configuration for JSON logging if desired, or richer text logging.
# For now, let's ensure a basic configuration that can be expanded.

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s [%(name)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": None, # Auto-detect based on tty
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(asctime)s [%(name)s] %(client_addr)s - "%(request_line)s" %(status_code)s',
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        # Example for JSON formatter (requires python-json-logger or similar)
        # "json": {
        #     "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
        #     "format": "%(asctime)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)d %(message)s"
        # }
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        # "json_handler": {
        #     "formatter": "json",
        #     "class": "logging.StreamHandler",
        #     "stream": "ext://sys.stdout"
        # }
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["default"], # or ["json_handler"] for JSON
            "level": "INFO",
            "propagate": False
        },
        "uvicorn.error": {
            "level": "INFO", # or "WARNING", "ERROR"
            "handlers": ["default"], # or ["json_handler"]
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["access"], # or ["json_handler"]
            "level": "INFO",
            "propagate": False,
        },
        "app": { # Your application's logger
            "handlers": ["default"], # or ["json_handler"]
            "level": "INFO", # Set to DEBUG for more verbose output from your app
            "propagate": False, # Prevent duplication if root logger also has handlers
        },
        # "alembic": { # Example for Alembic logger
        #     "handlers": ["default"],
        #     "level": "INFO",
        #     "propagate": False,
        # },
    },
    # "root": { # Optional: configure root logger
    #     "level": "WARNING",
    #     "handlers": ["default"], # or ["json_handler"]
    # }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)

# You would call setup_logging() in your main.py or a startup event.
# However, Uvicorn applies its own logging config by default.
# To override Uvicorn's default loggers, you often pass --log-config to uvicorn CLI
# or set `log_config` when running uvicorn programmatically.
# FastAPI doesn't directly control Uvicorn's logging config when Uvicorn is the entry point.

# For simplicity with docker-compose and uvicorn default command,
# Uvicorn's default structured logging to stdout is often sufficient for "basic".
# If JSON logging is strictly required, the setup is more involved, typically by
# either using a custom Uvicorn worker class or ensuring the log_config is passed.

# Let's add a simple logger for the app itself.
logger = logging.getLogger("app")
# Default level for app logger if not configured by dictConfig
# (though dictConfig above does configure it)
if not logger.hasHandlers(): # Avoid adding handlers if already configured by dictConfig
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# The current docker-compose uses `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
# This will use Uvicorn's default logging. To use LOGGING_CONFIG, we'd need to pass
# ` --log-config api/app/core/logging_config.py` (if it were a .ini or .json file)
# or set it up programmatically if running uvicorn.run().

# For now, Uvicorn's default stdout logging meets "basic structured logging".
# The code above is for future enhancement if specific JSON logging is needed.
# The `logger = logging.getLogger("app")` can be used throughout the app.
# e.g. from app.core.logging_config import logger; logger.info("message")
