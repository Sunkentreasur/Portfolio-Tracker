"""Portfolio Tracker - Main entry point.

This module is the main entry point for the Portfolio Tracker application.
It handles application initialization, creates the main window, and starts
the Qt event loop.
"""

import sys

from loguru import logger

from portfolio_manager.application.bootstrap import (
    create_qt_application,
    initialize_application,
)
from portfolio_manager.presentation.windows.main_window import MainWindow


def main() -> int:
    """Main application entry point.

    Returns:
        Exit code (0 for success, non-zero for error).
    """
    try:
        # Initialize application (configuration, logging, directories)
        initialize_application()

        # Create Qt application
        app = create_qt_application()

        # Create main window
        main_window = MainWindow()

        # Show main window
        main_window.show()

        # Start event loop
        logger.info("Starting event loop")
        exit_code = app.exec()

        logger.info(f"Application exiting with code: {exit_code}")
        return exit_code

    except Exception as e:
        logger.exception(f"Fatal error during application startup: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
