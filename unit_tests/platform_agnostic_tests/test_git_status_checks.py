"""Check the response to various states of the user's repository.

Should be able to use any valid platform for these calls.

Notes:
    There are a number of assertions about the state of the project as it's being set
    up. Arrange of AAA is critical, so those are in place to verify assumptions about
    the state of the project during setup.
"""

from pathlib import Path
import subprocess, shlex, os

import pytest

from ..utils import manage_sample_project as msp


# --- Fixtures ---

# --- Helper functions ---

def execute_quick_command(tmp_project, cmd):
    """Run a quick command, and return CompletedProcess object."""
    cmd_parts = shlex.split(cmd)
    os.chdir(tmp_project)
    return subprocess.run(cmd_parts, capture_output=True)

def add_sd_logs(tmp_project):
    """Add simple_deploy_logs/ dir, and a dummy log file with a single line."""
    log_dir = tmp_project / "simple_deploy_logs"
    assert not log_dir.exists()
    log_dir.mkdir()

    log_path = log_dir / "dummy_log.log"
    log_path.write_text("Dummy log entry.")

def add_sd_logs_gitignore(tmp_project):
    """Add simple_deploy_logs/ to .gitignore, without committing the change."""
    path = tmp_project / ".gitignore"
    assert path.exists()

    # simple_deploy_logs/ should not be in .gitignore yet.
    contents = path.read_text()
    assert "simple_deploy_logs" not in contents

    contents += "\nsimple_deploy_logs/\n"
    path.write_text(contents)

def add_sd_installed_apps(tmp_project):
    """Add simple_deploy to INSTALLED_APPS, as an uncommitted change.

    Run this before making other changes.
    """
    path = tmp_project / "blog" / "settings.py"
    settings_text = path.read_text()

    # It should already be there.
    assert "simple_deploy" in settings_text

    # Reset project to INITIAL_STATE, then add simple_deploy to INSTALLED_APPS without
    # committing.
    cmd = "git reset --hard INITIAL_STATE"
    output_str = execute_quick_command(tmp_project, cmd).stdout.decode()
    assert "HEAD is now at " in output_str
    assert "Initial commit." in output_str

    settings_lines = settings_text.splitlines()
    for index, line in enumerate(settings_lines):
        if "django-bootstrap5" in line:
            break

    settings_lines.insert(index+1, "    simple_deploy,")
    settings_text = "\n".join(settings_lines)
    path.write_text(settings_text)

    cmd = "git status --porcelain"
    output_str = execute_quick_command(tmp_project, cmd).stdout.decode()
    assert "M blog/settings.py" in output_str


# --- Test against various valid and invalid states of user's project. ---

def test_clean_git_status(tmp_project, capfd):
    """Call simple_deploy with the existing clean state of the project."""
    sd_command = "python manage.py simple_deploy --platform fly_io"
    stdout, stderr = msp.call_simple_deploy(tmp_project, sd_command)

    # This is only found if the git check passed.
    # DEV: Consider explicit output about git check that was run, or ignoring git status?
    assert   "Dependency management system: " in stdout

def test_unacceptable_settings_change(tmp_project, capfd):
    """Call simple_deploy after adding a non-simple_deploy line to settings.py."""
    path = tmp_project / "blog" / "settings.py"
    settings_text = path.read_text()
    new_text = "\n# Placeholder comment to create unacceptable git status."
    new_settings_text = settings_text + new_text
    path.write_text(new_settings_text)

    sd_command = "python manage.py simple_deploy --platform fly_io"
    stdout, stderr = msp.call_simple_deploy(tmp_project, sd_command)

    # This is only found if the git check passed.
    # DEV: Consider explicit output about git check that was run, or ignoring git status?
    assert   "Dependency management system: " not in stdout
    assert "SimpleDeployCommandError" in stderr

def test_unacceptable_file_changed(tmp_project, capfd):
    """Call simple_deploy after adding a comment to wsgi.py."""
    path = tmp_project / "blog" / "wsgi.py"
    wsgi_text = path.read_text()
    new_text = "\n# Placeholder comment to create unacceptable git status."
    new_wsgi_text = wsgi_text + new_text
    path.write_text(new_wsgi_text)

    sd_command = "python manage.py simple_deploy --platform fly_io"
    stdout, stderr = msp.call_simple_deploy(tmp_project, sd_command)

    # This is only found if the git check passed.
    # DEV: Consider explicit output about git check that was run, or ignoring git status?
    assert   "Dependency management system: " not in stdout
    assert "SimpleDeployCommandError" in stderr

def test_sdlogs_exists(tmp_project, capfd):
    """Add simple_deploy_logs/ dir, and dummy log file with one line."""
    add_sd_logs(tmp_project)

    sd_command = "python manage.py simple_deploy --platform fly_io"
    stdout, stderr = msp.call_simple_deploy(tmp_project, sd_command)

    # This is only found if the git check passed.
    # DEV: Consider explicit output about git check that was run, or ignoring git status?
    assert   "Dependency management system: " in stdout

def test_add_sdlogs_gitignore(tmp_project, capfd):
    """Add simple_deploy_logs/ to .gitignore."""
    add_sd_logs_gitignore(tmp_project)

    sd_command = "python manage.py simple_deploy --platform fly_io"
    stdout, stderr = msp.call_simple_deploy(tmp_project, sd_command)

    # This is only found if the git check passed.
    # DEV: Consider explicit output about git check that was run, or ignoring git status?
    assert   "Dependency management system: " in stdout

def test_add_sd_installed_apps(tmp_project, capfd):
    """Add simple_deploy to INSTALLED_APPS, as an uncommitted change."""
    add_sd_installed_apps(tmp_project)

    sd_command = "python manage.py simple_deploy --platform fly_io"
    stdout, stderr = msp.call_simple_deploy(tmp_project, sd_command)

    # This is only found if the git check passed.
    # DEV: Consider explicit output about git check that was run, or ignoring git status?
    assert   "Dependency management system: " in stdout

# --- Test combinations of two acceptable changes. ---

def test_sdlogs_exists_add_sdlogs_gitignore(tmp_project, capfd):
    """Add simple_deploy_logs/ dir, and dummy log file with one line. Also add sdlogs
    to .gitignore.
    """
    add_sd_logs(tmp_project)
    add_sd_logs_gitignore(tmp_project)

    sd_command = "python manage.py simple_deploy --platform fly_io"
    stdout, stderr = msp.call_simple_deploy(tmp_project, sd_command)

    # This is only found if the git check passed.
    # DEV: Consider explicit output about git check that was run, or ignoring git status?
    assert   "Dependency management system: " in stdout

def test_sdlogs_exists_sd_installed_apps(tmp_project, capfd):
    """Add simple_deploy_logs/ dir, and dummy log file with one line. Also add sd to
    INSTALLED_APPS.
    """
    # Order matters, because adding to INSTALLED_APPS starts by resetting project.
    add_sd_installed_apps(tmp_project)
    add_sd_logs(tmp_project)

    sd_command = "python manage.py simple_deploy --platform fly_io"
    stdout, stderr = msp.call_simple_deploy(tmp_project, sd_command)

    # This is only found if the git check passed.
    # DEV: Consider explicit output about git check that was run, or ignoring git status?
    assert   "Dependency management system: " in stdout

def test_sdlogs_gitignore_sd_installed_apps(tmp_project, capfd):
    """Add simple_deploy_logs/ to .gitignore, and  add sd to INSTALLED_APPS."""
    # Order matters, because adding to INSTALLED_APPS starts by resetting project.
    add_sd_installed_apps(tmp_project)
    add_sd_logs_gitignore(tmp_project)

    sd_command = "python manage.py simple_deploy --platform fly_io"
    stdout, stderr = msp.call_simple_deploy(tmp_project, sd_command)

    # This is only found if the git check passed.
    # DEV: Consider explicit output about git check that was run, or ignoring git status?
    assert   "Dependency management system: " in stdout

# --- Test combination of all three changes.

def test_sdlogs_exists_sdlogs_gitgnore_sd_installed_apps(tmp_project, capfd):
    """Add simple_deploy_logs/ dir and a single log file. Add simple_deploy_logs/ to
    .gitignore, and  add sd to INSTALLED_APPS.
    """
    # Order matters, because adding to INSTALLED_APPS starts by resetting project.
    add_sd_installed_apps(tmp_project)
    add_sd_logs(tmp_project)
    add_sd_logs_gitignore(tmp_project)

    sd_command = "python manage.py simple_deploy --platform fly_io"
    stdout, stderr = msp.call_simple_deploy(tmp_project, sd_command)

    # This is only found if the git check passed.
    # DEV: Consider explicit output about git check that was run, or ignoring git status?
    assert   "Dependency management system: " in stdout