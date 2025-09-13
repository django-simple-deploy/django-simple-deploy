"""Check that console output is what we expect it to be.

Should be able to use any valid platform for these calls.

This test was motivated by seeing every line of output doubled for an end
user who had logging configured to stream to stdout.
"""

from pathlib import Path
import subprocess, shlex, os, sys

import pytest

from ..utils import manage_sample_project as msp


# --- Helper functions ---


def execute_quick_command(tmp_project, cmd):
    """Run a quick command, and return CompletedProcess object."""
    cmd_parts = shlex.split(cmd)
    os.chdir(tmp_project)
    return subprocess.run(cmd_parts, capture_output=True)


# --- Test functions ---

def test_standard_output(tmp_project):
    """Test that output in a standard `deploy` call is correct.
    """
    # For now, this test only works if the dsd-flyio plugin is being tested.
    # Skip if that's not available.
    import importlib.util

    if not importlib.util.find_spec("dsd_flyio"):
        pytest.skip("The plugin dsd-flyio needs to be installed to run this test.")

    dsd_command = "python manage.py deploy"
    stdout, stderr = msp.call_deploy(tmp_project, dsd_command)

    # We shouldn't need to check for more specific output than this.
    expected_output_strings = [
        "Configuring project for deployment...\nLogging run of `manage.py deploy`...",
        "Deployment target: Fly.io\n  Using plugin: dsd_flyio",
         "--- Your project is now configured for deployment on Fly.io ---",
         "You can find a full record of this configuration in the dsd_logs directory.",
    ]

    for expected_string in expected_output_strings:
        assert expected_string in stdout



