"""Check the response to various states of the user's repository.

Should be able to use any valid platform for these calls.

Notes:
    There are a number of assertions about the state of the project as it's being set
    up. Arrange of AAA is critical, so those are in place to verify assumptions about
    the state of the project during setup.
"""

from pathlib import Path
import subprocess, shlex, os, sys

import pytest

from ..utils import manage_sample_project as msp


# --- Fixtures ---


@pytest.fixture(scope="function", autouse=True)
def reset_test_project_function(request, tmp_project):
    """Function-scoped version of reset_test_project().

    This is used in modules where the project needs to be reset for each test.

    Reset the test project, so it can be used again by another test module,
    which may be another platform.
    """
    # All of the work done for checking git status happens before a package manager is
    # even identified. So, should be able to run tests against just one pkg_manager.
    # If a test starts to fail for only one pkg_manager, parametrize this fixture.
    msp.reset_test_project(tmp_project, "req_txt")


@pytest.fixture(autouse=True)
def run_simple_deploy():
    """Overrides main run_simple_deploy() fixture, which is not needed here."""
    return


# --- Helper functions ---


def execute_quick_command(tmp_project, cmd):
    """Run a quick command, and return CompletedProcess object."""
    cmd_parts = shlex.split(cmd)
    os.chdir(tmp_project)
    return subprocess.run(cmd_parts, capture_output=True)


def add_sd_logs(tmp_project):
    """Add dsd_logs/ dir, and a dummy log file with a single line."""
    log_dir = tmp_project / "dsd_logs"
    assert not log_dir.exists()
    log_dir.mkdir()

    log_path = log_dir / "dummy_log.log"
    log_path.write_text("Dummy log entry.")


def add_sd_logs_gitignore(tmp_project):
    """Add dsd_logs/ to .gitignore, without committing the change."""
    path = tmp_project / ".gitignore"
    assert path.exists()

    # dsd_logs/ should not be in .gitignore yet.
    contents = path.read_text()
    assert "dsd_logs" not in contents

    contents += "\ndsd_logs/\n"
    path.write_text(contents)


def add_sd_installed_apps(tmp_project):
    """Add django_simple_deploy to INSTALLED_APPS, as an uncommitted change.

    Run this before making other changes.
    """
    # Reset project to INITIAL_STATE, to remove django_simple_deploy from INSTALLED_APPS.
    cmd = "git reset --hard INITIAL_STATE"
    output_str = execute_quick_command(tmp_project, cmd).stdout.decode()
    assert "HEAD is now at " in output_str
    assert "Initial commit." in output_str

    path = tmp_project / "blog" / "settings.py"
    settings_text = path.read_text()

    # 'django_simple_deploy' should no longer be in settings.
    assert "django_simple_deploy" not in settings_text

    # Split settings into lines, and find where to insert 'django_simple_deploy'.
    settings_lines = settings_text.splitlines()
    for index, line in enumerate(settings_lines):
        if "django_bootstrap5" in line:
            break

    settings_lines.insert(index + 1, '    "django_simple_deploy",')
    settings_text = "\n".join(settings_lines)
    # Add back the trailing newline that was lost in text processing.
    settings_text += "\n"
    path.write_text(settings_text)

    cmd = "git status --porcelain"
    output_str = execute_quick_command(tmp_project, cmd).stdout.decode()
    assert "M blog/settings.py" in output_str


# --- Tests without --ignore-unclean-git flag. ---


def test_clean_git_status(tmp_project):
    """Call deploy with the existing clean state of the project."""
    dsd_command = "python manage.py deploy"
    stdout, stderr = msp.call_deploy(tmp_project, dsd_command)

    assert "No uncommitted changes, other than django-simple-deploy work." in stdout


def test_unacceptable_settings_change(tmp_project):
    """Call deploy after adding a non-dsd line to settings.py."""
    path = tmp_project / "blog" / "settings.py"
    settings_text = path.read_text()
    new_text = "\n# Placeholder comment to create unacceptable git status.\n"
    new_settings_text = settings_text + new_text
    path.write_text(new_settings_text)

    dsd_command = "python manage.py deploy"
    stdout, stderr = msp.call_deploy(tmp_project, dsd_command)

    assert "No uncommitted changes, other than django-simple-deploy work." not in stdout
    assert "DSDCommandError" in stderr


def test_unacceptable_file_changed(tmp_project):
    """Call deploy after adding a comment to wsgi.py."""
    path = tmp_project / "blog" / "wsgi.py"
    wsgi_text = path.read_text()
    new_text = "\n# Placeholder comment to create unacceptable git status."
    new_wsgi_text = wsgi_text + new_text
    path.write_text(new_wsgi_text)

    dsd_command = "python manage.py deploy"
    stdout, stderr = msp.call_deploy(tmp_project, dsd_command)

    assert "No uncommitted changes, other than django-simple-deploy work." not in stdout
    assert "DSDCommandError" in stderr


def test_sdlogs_exists(tmp_project):
    """Add dsd_logs/ dir, and dummy log file with one line."""
    add_sd_logs(tmp_project)

    dsd_command = "python manage.py deploy"
    stdout, stderr = msp.call_deploy(tmp_project, dsd_command)

    assert "No uncommitted changes, other than django-simple-deploy work." in stdout


def test_add_sdlogs_gitignore(tmp_project):
    """Add dsd_logs/ to .gitignore."""
    add_sd_logs_gitignore(tmp_project)

    dsd_command = "python manage.py deploy"
    stdout, stderr = msp.call_deploy(tmp_project, dsd_command)

    assert "No uncommitted changes, other than django-simple-deploy work." in stdout


def test_add_sd_installed_apps(tmp_project):
    """Add django_simple_deploy to INSTALLED_APPS, as an uncommitted change."""
    add_sd_installed_apps(tmp_project)

    dsd_command = "python manage.py deploy"
    stdout, stderr = msp.call_deploy(tmp_project, dsd_command)

    assert "No uncommitted changes, other than django-simple-deploy work." in stdout


# --- Test combinations of two acceptable changes. ---


def test_sdlogs_exists_add_sdlogs_gitignore(tmp_project):
    """Add dsd_logs/ dir, and dummy log file with one line. Also add sdlogs
    to .gitignore.
    """
    add_sd_logs(tmp_project)
    add_sd_logs_gitignore(tmp_project)

    dsd_command = "python manage.py deploy"
    stdout, stderr = msp.call_deploy(tmp_project, dsd_command)

    assert "No uncommitted changes, other than django-simple-deploy work." in stdout


def test_sdlogs_exists_sd_installed_apps(tmp_project):
    """Add dsd_logs/ dir, and dummy log file with one line. Also add sd to
    INSTALLED_APPS.
    """
    # Order matters, because adding to INSTALLED_APPS starts by resetting project.
    add_sd_installed_apps(tmp_project)
    add_sd_logs(tmp_project)

    dsd_command = "python manage.py deploy"
    stdout, stderr = msp.call_deploy(tmp_project, dsd_command)

    assert "No uncommitted changes, other than django-simple-deploy work." in stdout


def test_sdlogs_gitignore_sd_installed_apps(tmp_project):
    """Add dsd_logs/ to .gitignore, and  add sd to INSTALLED_APPS."""
    # Order matters, because adding to INSTALLED_APPS starts by resetting project.
    add_sd_installed_apps(tmp_project)
    add_sd_logs_gitignore(tmp_project)

    dsd_command = "python manage.py deploy"
    stdout, stderr = msp.call_deploy(tmp_project, dsd_command)

    assert "No uncommitted changes, other than django-simple-deploy work." in stdout


# --- Test combination of all three changes.


def test_sdlogs_exists_sdlogs_gitgnore_sd_installed_apps(tmp_project):
    """Add dsd_logs/ dir and a single log file. Add dsd_logs/ to
    .gitignore, and  add sd to INSTALLED_APPS.
    """
    # Order matters, because adding to INSTALLED_APPS starts by resetting project.
    add_sd_installed_apps(tmp_project)
    add_sd_logs(tmp_project)
    add_sd_logs_gitignore(tmp_project)

    dsd_command = "python manage.py deploy"
    stdout, stderr = msp.call_deploy(tmp_project, dsd_command)

    assert "No uncommitted changes, other than django-simple-deploy work." in stdout


# --- Tests using --ignore-unclean-git flag. ---


def test_clean_git_status_ignore_unclean_flag(tmp_project):
    """Call deploy with the existing clean state of the project."""
    dsd_command = "python manage.py deploy --ignore-unclean-git"
    stdout, stderr = msp.call_deploy(tmp_project, dsd_command)

    assert "Ignoring git status." in stdout


def test_unacceptable_settings_change_ignore_unclean_flag(tmp_project):
    """Call deploy after adding a non-dsd line to settings.py."""
    path = tmp_project / "blog" / "settings.py"
    settings_text = path.read_text()
    new_text = "\n# Placeholder comment to create unacceptable git status."
    new_settings_text = settings_text + new_text
    path.write_text(new_settings_text)

    dsd_command = "python manage.py deploy --ignore-unclean-git"
    stdout, stderr = msp.call_deploy(tmp_project, dsd_command)

    assert "Ignoring git status." in stdout
    # assert "Ignoring git status." not in stdout


def test_unacceptable_file_changed_ignore_unclean_flag(tmp_project):
    """Call deploy after adding a comment to wsgi.py."""
    path = tmp_project / "blog" / "wsgi.py"
    wsgi_text = path.read_text()
    new_text = "\n# Placeholder comment to create unacceptable git status."
    new_wsgi_text = wsgi_text + new_text
    path.write_text(new_wsgi_text)

    dsd_command = "python manage.py deploy --ignore-unclean-git"
    stdout, stderr = msp.call_deploy(tmp_project, dsd_command)

    assert "Ignoring git status." in stdout
