"""
Console formatting utilities for GLOFNet.

These helpers provide consistent, readable output across
exploration scripts and data pipelines.

Example:
    >>> print_header("ITS_LIVE STAC Exploration")
    >>> print_section("Bounding Box")
    >>> print_key_value("West", 74.52)
    >>> print_success("Connected to STAC")
"""

from typing import Any, Iterable

HEADER_WIDTH = 70
HEADER_CHAR = "="
SECTION_CHAR = "-"


def print_header(title: str) -> None:
    """Print a major section header."""
    print()
    print(HEADER_CHAR * HEADER_WIDTH)
    print(title)
    print(HEADER_CHAR * HEADER_WIDTH)


def print_section(title: str) -> None:
    """Print a subsection header."""
    print()
    print(SECTION_CHAR * HEADER_WIDTH)
    print(title)
    print(SECTION_CHAR * HEADER_WIDTH)


def print_key_value(key: str, value: Any, width: int = 20) -> None:
    """
    Print a formatted key-value pair.

    Example:
        Glacier ID          : RGI60-13.12345
        Collection          : itslive-cubes
    """
    print(f"{key:<{width}} : {value}")


def print_list(title: str, items: Iterable[Any]) -> None:
    """
    Print a titled bullet list.

    Example:
        Assets
        ------
          • zarr
          • thumbnail
          • metadata
    """
    print_section(title)

    items = list(items)

    if not items:
        print("  (none)")
        return

    for item in items:
        print(f"  • {item}")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"✓ {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"⚠ {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"✗ {message}")