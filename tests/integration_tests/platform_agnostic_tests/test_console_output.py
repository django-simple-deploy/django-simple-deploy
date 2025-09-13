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

    # Make sure output is not doubled (ie logging written to log and stdout).
    for expected_string in expected_output_strings:
        assert expected_string in stdout
        assert stdout.count(expected_string) == 1

@pytest.mark.skip("Needs more config to test behavior correctly.")
def test_logging_streaming_to_stdout(tmp_project):
    """Test that output is not doubled when logging is configured to stream to stdout.

    DEV: The interaction between pytest, logging, and stdout is more complex than this
    test currently represents. To actually detect doubled output, this test needs to 
    intercept the logging stream that pytest captures as well as stdout. That doesn't seem
    worthwhile at the moment. If there are more issues with doubled output, we can revisit
    this.
    """
    # For now, this test only works if the dsd-flyio plugin is being tested.
    # Skip if that's not available.
    import importlib.util

    if not importlib.util.find_spec("dsd_flyio"):
        pytest.skip("The plugin dsd-flyio needs to be installed to run this test.")

    # Modify sample project settings before calling deploy.
    logging_setting = "LOGGING = {'version': 1, 'handlers': {'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler'}}, 'root': {'handlers': ['console'], 'level': 'DEBUG'}}\n"
    path_settings = tmp_project / "blog" / "settings.py"
    settings_lines = path_settings.read_text().splitlines()

    settings_lines.insert(12, logging_setting)
    content_settings_modified = "\n".join(settings_lines) + "\n"
    path_settings.write_text(content_settings_modified)

    # Commit this change, so deploy is called against a clean git status.
    cmd = "git commit -am 'Configured logging to stream to stdout.'"
    output_str = execute_quick_command(tmp_project, cmd).stdout.decode()

    # Run deploy against project with logging configured to stream to stdout.
    dsd_command = "python manage.py deploy"
    stdout, stderr = msp.call_deploy(tmp_project, dsd_command)

    # We shouldn't need to check for more specific output than this.
    expected_output_strings = [
        "Configuring project for deployment...\nLogging run of `manage.py deploy`...",
        "Deployment target: Fly.io\n  Using plugin: dsd_flyio",
         "--- Your project is now configured for deployment on Fly.io ---",
         "You can find a full record of this configuration in the dsd_logs directory.",
    ]

    # Make sure output is not doubled (ie logging written to log and stdout).
    for expected_string in expected_output_strings:
        assert expected_string in stdout
        assert stdout.count(expected_string) == 1