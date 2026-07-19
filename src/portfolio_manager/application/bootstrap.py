"""Application bootstrap module.

This module handles the application startup sequence including configuration
loading, logging initialization, and QApplication creation.
"""

import sys

from loguru import logger

from portfolio_manager.infrastructure.config.settings import config
from portfolio_manager.infrastructure.logging.logger import LogConfig


def initialize_application() -> None:
    """Initialize the application before UI creation.

    This method performs all necessary initialization steps:
    - Ensure required directories exist
    - Configure logging
    - Load application configuration

    Should be called before creating the QApplication.
    """
    logger.info(f"Starting {config.APP_NAME} v{config.VERSION}")

    # Ensure all required directories exist
    config.ensure_directories()
    logger.debug(f"User data directory: {config.USER_DATA_DIR}")
    logger.debug(f"Database path: {config.DATABASE_PATH}")

    # Configure logging
    LogConfig.setup()

    logger.info("Application initialization complete")


def create_qt_application() -> "QApplication":
    """Create and configure the QApplication instance.

    Returns:
        A configured QApplication instance ready for use.

    Raises:
        ImportError: If PySide6 is not available.
    """
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError as e:
        logger.error("PySide6 is not installed")
        raise ImportError(
            "PySide6 is required. Install it with: pip install PySide6"
        ) from e

    # Create QApplication
    app = QApplication(sys.argv)

    # Set application metadata
    app.setApplicationName(config.APP_NAME)
    app.setApplicationVersion(config.VERSION)
    app.setOrganizationName(config.APP_ID)

    logger.info("QApplication created")

    return app
