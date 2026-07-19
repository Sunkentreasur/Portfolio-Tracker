"""Application configuration module.

This module provides centralized configuration management for Portfolio Tracker.
All global configuration values are defined here to avoid hardcoded values throughout
the project.
"""

from pathlib import Path
from typing import Final

from platformdirs import AppDirs


class AppConfig:
    """Centralized application configuration.

    This class provides access to all global configuration values including
    paths, application metadata, and settings. Configuration is loaded once
    at application startup and remains immutable during runtime.
    """

    # Application metadata
    APP_NAME: Final[str] = "Portfolio Tracker"
    APP_ID: Final[str] = "com.portfoliotracker.app"
    VERSION: Final[str] = "0.1.0"

    # Directory configuration
    _app_dirs: Final[AppDirs] = AppDirs(appname=APP_NAME, appid=APP_ID)

    USER_DATA_DIR: Final[Path] = Path(_app_dirs.user_data_dir)
    LOG_DIR: Final[Path] = Path(_app_dirs.user_log_dir)
    CONFIG_DIR: Final[Path] = Path(_app_dirs.user_config_dir)

    # Database configuration
    DATABASE_DIR: Final[Path] = USER_DATA_DIR / "data"
    DATABASE_PATH: Final[Path] = DATABASE_DIR / "portfolio.db"

    # Logging configuration
    LOG_FILE: Final[Path] = LOG_DIR / "portfolio_tracker.log"
    LOG_ROTATION_SIZE: Final[str] = "10 MB"
    LOG_RETENTION_COUNT: Final[int] = 5

    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure all required directories exist.

        Creates the user data directory, log directory, and database directory
        if they do not already exist. This should be called during application
        startup.
        """
        cls.USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        cls.DATABASE_DIR.mkdir(parents=True, exist_ok=True)


# Global configuration instance
config = AppConfig()
