"""Check the output of valid platform-agnostic cli commands."""

from pathlib import Path
import subprocess

import pytest

from ..utils import manage_sample_project as msp


# --- Fixtures ---

# --- Helper functions ---


# --- Test valid platform-agnostic deploy calls ---


def test_help_output(tmp_project, capfd):
    """Call `manage.py deploy --help`."""
    valid_dsd_command = "python manage.py deploy --help"
    stdout, stderr = msp.call_deploy(tmp_project, valid_dsd_command)

    current_test_dir = Path(__file__).parent
    reference_help_output = (
        current_test_dir / "reference_files/sd_help_output.txt"
    ).read_text()

    # Plugins may add CLI args, which means they can modify help output.
    # So, we can only check for individual lines from core that should
    # appear in help output, not entire output.
    help_lines = [l for l in reference_help_output.splitlines() if l]

    for help_line in help_lines:
        assert help_line in stdout
