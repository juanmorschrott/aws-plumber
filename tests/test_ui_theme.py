"""Tests for UI theme."""

from aws_plumber.ui.theme import (
    format_selection_menu,
    ACCENT_COLOR,
    GRAY_TEXT,
    SUCCESS_COLOR,
    ERROR_COLOR,
)


def test_format_selection_menu():
    """Test menu formatting."""
    items = ["Option 1", "Option 2", "Option 3"]
    menu = format_selection_menu(items, selected_index=1)
    assert "► Option 2" in menu
    assert "  Option 1" in menu
    assert "  Option 3" in menu


def test_color_constants():
    """Test color constants are defined."""
    assert ACCENT_COLOR == "#ccff00"
    assert GRAY_TEXT == "#c0c0c0"
    assert SUCCESS_COLOR == "#00ff00"
    assert ERROR_COLOR == "#ff0000"

