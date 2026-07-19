"""Main application window.

This module provides the main application window for Portfolio Tracker.
The window includes a menu bar, status bar, and empty central widget.
No business logic is implemented at this stage.
"""

from loguru import logger

from portfolio_manager.infrastructure.config.settings import config


class MainWindow:
    """Main application window.

    A minimal PySide6 main window with title, menu bar, status bar,
    and empty central widget. Business logic will be added in future phases.
    """

    def __init__(self) -> None:
        """Initialize the main window."""
        try:
            from PySide6.QtWidgets import (
                QMainWindow,
                QMenuBar,
                QStatusBar,
                QWidget,
            )
        except ImportError as e:
            logger.error("PySide6 is not installed")
            raise ImportError(
                "PySide6 is required. Install it with: pip install PySide6"
            ) from e

        self._window = QMainWindow()
        self._setup_window()
        self._setup_menu_bar()
        self._setup_status_bar()
        self._setup_central_widget()

        logger.info("Main window created")

    def _setup_window(self) -> None:
        """Configure window properties."""
        self._window.setWindowTitle(config.APP_NAME)
        self._window.resize(1200, 800)
        self._window.setMinimumSize(800, 600)

    def _setup_menu_bar(self) -> None:
        """Create and configure the menu bar."""
        menu_bar = QMenuBar(self._window)
        self._window.setMenuBar(menu_bar)

        # File menu
        file_menu = menu_bar.addMenu("&File")

        # Edit menu
        edit_menu = menu_bar.addMenu("&Edit")

        # View menu
        view_menu = menu_bar.addMenu("&View")

        # Help menu
        help_menu = menu_bar.addMenu("&Help")

    def _setup_status_bar(self) -> None:
        """Create and configure the status bar."""
        status_bar = QStatusBar(self._window)
        self._window.setStatusBar(status_bar)
        status_bar.showMessage("Ready")

    def _setup_central_widget(self) -> None:
        """Create and configure the central widget."""
        central_widget = QWidget(self._window)
        self._window.setCentralWidget(central_widget)

    @property
    def qt_window(self) -> "QMainWindow":
        """Return the underlying QMainWindow instance.

        Returns:
            The PySide6 QMainWindow instance.
        """
        return self._window

    def show(self) -> None:
        """Show the main window."""
        self._window.show()
        logger.info("Main window shown")
