import os
import subprocess
import sys
import importlib
from pathlib import Path
from shutil import copytree, rmtree
from shlex import split

from django_simple_deploy.management.commands.utils import dsd_utils

import pytest


def setup_project(tmp_proj_dir, sd_root_dir, config):
    """Set up the test project.
    - Copy the sample project to a temp dir.
    - Set up a venv.
    - Install requirements for the sample project.
    - Install the local, editable version of django-simple-deploy.
    - Make an initial commit.
    - Add django_simple_deploy to INSTALLED_APPS.

    Returns:
    - None
    """
    # Find out if uv is available.
    try:
        subprocess.run(["uv", "--version"])
    except FileNotFoundError:
        uv_available = False
    else:
        uv_available = True

    # Copy sample project to temp dir.
    sample_project_dir = sd_root_dir / "sample_project/blog_project"
    copytree(sample_project_dir, tmp_proj_dir, dirs_exist_ok=True)

    # Create a virtual envronment. Set the path to the environment, instead of
    #   activating it. It's easier to use the venv directly than to activate it,
    #   with all these separate subprocess.run() calls.
    venv_dir = tmp_proj_dir / "b_env"
    if uv_available:
        subprocess.run(["uv", "venv", venv_dir])
    else:
        subprocess.run([sys.executable, "-m", "venv", venv_dir])

    # Install requirements for sample project, from vendor/.
    #   Don't upgrade pip, as that would involve a network call. When troubleshooting,
    #   keep in mind someone at some point might just need to upgrade their pip.
    requirements_path = tmp_proj_dir / "requirements.txt"

    if uv_available:
        path_to_python = venv_dir / "bin" / "python"
        if sys.platform == "win32":
            path_to_python = venv_dir / "Scripts" / "python.exe"
        subprocess.run(
            [
                "uv",
                "pip",
                "install",
                "--python",
                path_to_python,
                "--no-index",
                "--find-links",
                sd_root_dir / "vendor",
                "-r",
                requirements_path,
            ]
        )
    else:
        pip_path = venv_dir / ("Scripts" if os.name == "nt" else "bin") / "pip"
        subprocess.run(
            [
                pip_path,
                "install",
                "--no-index",
                "--find-links",
                sd_root_dir / "vendor",
                "-r",
                requirements_path,
            ]
        )

    # Install the local version of django-simple-deploy (the version we're testing).
    # An editable install is preferred for two reasons. It's much faster than a non-editable
    # install. It also makes the temp test project *really* useful for debugging, and even
    # development. You can run a test, maybe `pytest -x`, drop into the temp project and
    # activate the venv, and then run the deploy command while fixing the bug.
    if uv_available:
        subprocess.run(
            ["uv", "pip", "install", "--python", path_to_python, "-e", sd_root_dir]
        )
    else:
        subprocess.run([pip_path, "install", "-e", sd_root_dir])

    # Install editable versions of default plugins that are available.
    # DEV: I believe dsd-flyio is required for core integration testing. Ensure that
    # it's available. Also, consider emitting warning if any default plugins are not
    # being tested.
    # Assumes user has default plugins in repos named dsd-flyio, in same directory as
    # their development copy of django-simple-deploy.
    # default_plugin_names = ["dsd-flyio", "dsd-platformsh", "dsd-heroku"]
    # DEV: Hacky [:1] insertion to just test against dsd-flyio plugin for now.
    # Need to determine which plugin to install for testing.
    # for plugin_name in default_plugin_names[:1]:
    #     plugin_root_dir = sd_root_dir.parent / plugin_name

    #     if not plugin_root_dir.exists():
    #         print(f"Can't install default plugin {plugin_name}.")
    #         continue

    #     if uv_available:
    #         subprocess.run(
    #             [
    #                 "uv",
    #                 "pip",
    #                 "install",
    #                 "--python",
    #                 path_to_python,
    #                 "-e",
    #                 plugin_root_dir,
    #             ]
    #         )
    #     else:
    #         subprocess.run([pip_path, "install", "-e", plugin_root_dir])

    # Install a plugin. If no plugin specified, install local editable version of dsd-flyio.
    # If a plugin specified, install same version that's installed to dev env.
    # DEV: This approach is breaking tests for other plugins.
    #   Better: install whatever plugin is installed locally.
    plugin = config.option.plugin
    if config.option.plugin is None:
        plugin = dsd_utils.get_plugin_name()
        print("plugin", plugin)
        # breakpoint()
        # pytest.exit()

    plugin_pkg_name = plugin.replace("-", "_")
    try:
        plugin_module = importlib.import_module(plugin_pkg_name)
    except ImportError:
        msg = f"The plugin {plugin} is not installed. You must install a plugin in editable mode in order to test it."
        pytest.fail(msg)

    # breakpoint()
    plugin_path = Path(plugin_module.__file__).parents[1]

    if not plugin_path.exists():
        msg = f"Can't install plugin {plugin}. A plugin must be installed to run integration test."
        pytest.exit(msg)

    if uv_available:
        subprocess.run(
            [
                "uv",
                "pip",
                "install",
                "--python",
                path_to_python,
                "-e",
                plugin_path,
            ]
        )
    else:
        subprocess.run([pip_path, "install", "-e", plugin_path])

    # breakpoint()

    # Make an initial git commit, so we can reset the project every time we want
    #   to test a different deploy command. This is much more efficient than
    #   tearing down the whole sample project and rebuilding it from scratch.
    # We use a git tag to do the reset, instead of trying to capture the initial hash.
    # Note: This tag refers to the version of the project that contains files for all
    #   dependency management systems, ie requirements.txt, pyproject.toml, and Pipfile.
    git_exe = "git"
    os.chdir(tmp_proj_dir)
    subprocess.run([git_exe, "init"])
    subprocess.run([git_exe, "branch", "-m", "main"])
    subprocess.run([git_exe, "add", "."])
    subprocess.run([git_exe, "commit", "-am", "Initial commit."])
    subprocess.run([git_exe, "tag", "-am", "", "INITIAL_STATE"])

    # Add django_simple_deploy to INSTALLED_APPS.
    settings_file_path = tmp_proj_dir / "blog/settings.py"
    settings_content = settings_file_path.read_text()
    new_settings_content = settings_content.replace(
        "# Third party apps.", '# Third party apps.\n    "django_simple_deploy",'
    )
    settings_file_path.write_text(new_settings_content)


def reset_test_project(tmp_dir, pkg_manager):
    """Reset the test project, so it's ready to be used by another test module.
    It may be used by a different platform than the previous run.
    """

    os.chdir(tmp_dir)

    # Reset to the initial state of the temp project instance.
    subprocess.run(["git", "reset", "--hard", "INITIAL_STATE"])
    subprocess.run(["git", "clean", "-fd"])

    # Remove dependency management files not needed for this package manager
    if pkg_manager == "req_txt":
        (tmp_dir / "pyproject.toml").unlink()
        (tmp_dir / "Pipfile").unlink()
    elif pkg_manager == "poetry":
        (tmp_dir / "requirements.txt").unlink()
        (tmp_dir / "Pipfile").unlink()
    elif pkg_manager == "pipenv":
        (tmp_dir / "requirements.txt").unlink()
        (tmp_dir / "pyproject.toml").unlink()

    # Commit these changes; helpful in diagnosing failed runs, when you cd into the test
    #   project directory and run git status.
    subprocess.run(
        ["git", "commit", "-am", "Removed unneeded dependency management files."]
    )

    # Add django_simple_deploy to INSTALLED_APPS.
    settings_file_path = tmp_dir / "blog/settings.py"
    settings_content = settings_file_path.read_text()
    new_settings_content = settings_content.replace(
        "# Third party apps.", '# Third party apps.\n    "django_simple_deploy",'
    )
    settings_file_path.write_text(new_settings_content)

    # Make sure we have a clean status before calling deploy.
    subprocess.run(
        ["git", "commit", "-am", "Added django_simple_deploy to INSTALLED_APPS."]
    )


def call_deploy(tmp_dir, dsd_command, platform=None):
    """Make a call to deploy, using the arguments passed in dsd_command.

    Returns:
    - stdout, stderr

    These are both strings.
    """

    # Change to the temp dir.
    os.chdir(tmp_dir)

    # Add --unit-testing argument to the call.
    dsd_command = dsd_command.replace("deploy", "deploy --unit-testing")

    # Add options that are present.
    # - If we're testing for a platform, add that platform option.
    # - Some platforms require a deployed project name, which isn't inferred from
    #   the project being deployed. This is typically because the platform generates
    #   a project name, ie misty-fjords-12345 during actual deployment.
    # Automated testing tends to use platform names like flyio, derived from repository
    # path. But manual use of integration test utilities may still use the form fly_io,
    # so keep both for now.
    # DEV: This will probably not be hard-coded once third-party plugins are being
    # written.
    if platform:
        dsd_command = f"{dsd_command}"
    if platform in ("fly_io", "flyio", "platform_sh", "platformsh"):
        # These platforms need a project name to carry out configuration.
        dsd_command = f"{dsd_command} --deployed-project-name my_blog_project"

    # Get the path to the Python interpreter in the virtual environment.
    #   We'll use the full path to the interpreter, rather than trying to rely on
    #   an active venv.
    if sys.platform == "win32":
        python_exe = Path(tmp_dir) / "b_env" / "Scripts" / "python.exe"
    else:
        python_exe = Path(tmp_dir) / "b_env" / "bin" / "python"

    dsd_command = dsd_command.replace("python", python_exe.as_posix())
    print(f"*** dsd_command: {dsd_command} ***")

    # Make the call to deploy.
    #   The `text=True` argument causes this to return stdout and stderr as strings, not objects.
    #   Some of these commands, such as cwd, are required specifically for Windows.
    sd_call = subprocess.Popen(
        split(dsd_command),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=tmp_dir,
    )
    stdout, stderr = sd_call.communicate()

    return stdout, stderr


def make_git_call(tmp_dir, git_call):
    """Make a git call against the test project.
    Returns:
    - stdout, stderr as strings.
    """
    os.chdir(tmp_dir)
    git_call_object = subprocess.Popen(
        split(git_call), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout, stderr = git_call_object.communicate()

    return stdout, stderr
