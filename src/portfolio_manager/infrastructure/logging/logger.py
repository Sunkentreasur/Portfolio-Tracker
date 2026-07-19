"""Application logging configuration.

This module provides centralized logging configuration using loguru.
Logging is configured once during application startup and provides both
console and file logging with rotation.
"""

import sys
from pathlib import Path
from typing import Final

from loguru import logger

from portfolio_manager.infrastructure.config.settings import config


class LogConfig:
    """Logging configuration for Portfolio Tracker.

    Configures loguru to provide structured logging with console output
    and rotating file logs. Sensitive user data is never logged.
    """

    # Log format
    LOG_FORMAT: Final[str] = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    @classmethod
    def setup(cls) -> None:
        """Configure application-wide logging.

        This method:
        - Removes the default loguru handler
        - Adds console logging with INFO level
        - Adds file logging with rotation
        - Ensures log directory exists

        Should be called once during application bootstrap.
        """
        # Ensure log directory exists
        config.LOG_DIR.mkdir(parents=True, exist_ok=True)

        # Remove default handler
        logger.remove()

        # Add console handler
        logger.add(
            sys.stderr,
            format=cls.LOG_FORMAT,
            level="INFO",
            colorize=True,
        )

        # Add file handler with rotation
        logger.add(
            config.LOG_FILE,
            format=cls.LOG_FORMAT,
            level="DEBUG",
            rotation=config.LOG_ROTATION_SIZE,
            retention=config.LOG_RETENTION_COUNT,
            compression="zip",
            encoding="utf-8",
        )

        logger.info(f"Logging initialized. Log file: {config.LOG_FILE}")


def get_logger(name: str) -> "logger":
    """Get a logger instance for a specific module.

    Args:
        name: The module name (typically __name__)

    Returns:
        A loguru logger instance configured for the module.
    """
    return logger.bind(name=name)
