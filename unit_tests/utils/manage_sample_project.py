import os
import subprocess
import sys
from pathlib import Path
from shutil import copytree, rmtree
from shlex import split

def setup_project(tmp_proj_dir, sd_root_dir):
    """Set up the test project.
    - Copy the sample project to a temp dir.
    - Set up a venv.
    - Install requiremenst for the sample project.
    - Install the local, editable version of simple_deploy.
    - Make an initial commit.
    - Add simple_deploy to INSTALLED_APPS.

    Returns:
    - None
    """

    # Copy sample project to temp dir.
    sample_project_dir = sd_root_dir / "sample_project/blog_project"
    copytree(sample_project_dir, tmp_proj_dir, dirs_exist_ok=True)

    # Create a virtual envronment. Set the path to the environemnt, instead of
    #   activating it. It's easier to use the venv directly than to activate it,
    #   with all these separate subprocess.run() calls.
    venv_dir = tmp_proj_dir / "b_env"
    subprocess.run([sys.executable, "-m", "venv", venv_dir])

    # Install requirements for sample project, from vendor/.
    #   Don't upgrade pip, as that would involve a network call. When troubleshooting,
    #   keep in mind someone at some point might just need to upgrade their pip.
    pip_path = venv_dir / ("Scripts" if os.name == "nt" else "bin") / "pip"
    requirements_path = tmp_proj_dir / "requirements.txt"
    subprocess.run([pip_path, "install", "--no-index", "--find-links", sd_root_dir / "vendor", "-r", requirements_path])

    # Install the local version of simple_deploy (the version we're testing).
    # Note: We don't need an editable install, but a non-editable install is *much* slower.
    #   We may be able to use --cache-dir to address this, but -e is working fine right now.
    subprocess.run([pip_path, "install", "-e", sd_root_dir])

    # Make an initial git commit, so we can reset the project every time we want
    #   to test a different simple_deploy command. This is much more efficient than
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

    # Add simple_deploy to INSTALLED_APPS.
    settings_file_path = tmp_proj_dir / "blog/settings.py"
    settings_content = settings_file_path.read_text()
    new_settings_content = settings_content.replace("# Third party apps.", "# Third party apps.\n    'simple_deploy',")
    settings_file_path.write_text(new_settings_content)


def reset_test_project(tmp_dir, pkg_manager):
    os.chdir(tmp_dir)

    # Reset to the initial state of the temp project instance
    subprocess.run(["git", "reset", "--hard", "INITIAL_STATE"])

    # Remove any files that may remain
    files_to_remove = [
        "fly.toml",
        "Dockerfile",
        ".dockerignore",
        ".platform.app.yaml",
        "Procfile",
        "poetry.lock",
    ]

    dirs_to_remove = [
        ".platform",
        "static",
        "simple_deploy_logs",
        "__pycache__",
    ]

    for file in files_to_remove:
        file_path = Path(tmp_dir) / file
        if file_path.is_file():
            file_path.unlink()

    for directory in dirs_to_remove:
        dir_path = Path(tmp_dir) / directory
        if dir_path.is_dir():
            rmtree(dir_path)

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

    # Commit changes
    subprocess.run(["git", "commit", "-am", "Removed unneeded dependency management files."])

    # Add simple_deploy to INSTALLED_APPS
    settings_file_path = tmp_dir / "blog/settings.py"
    settings_content = settings_file_path.read_text()
    new_settings_content = settings_content.replace("# Third party apps.", "# Third party apps.\n    'simple_deploy',")
    settings_file_path.write_text(new_settings_content)

    # Make sure we have a clean status before calling simple_deploy
    subprocess.run(["git", "commit", "-am", "Added simple_deploy to INSTALLED_APPS."])


def call_simple_deploy(tmp_dir, sd_command, platform=None):
    """Make a call to simple_deploy, using the arguments passed in sd_command.

    Returns:
    - stdout, stderr

    These are both strings.
    """

    # Change to the temp dir.
    os.chdir(tmp_dir)

    # Add options that are present.
    if platform:
        sd_command = f"{sd_command} --platform {platform}"
    if platform in ('fly_io', 'platform_sh'):
        # These platforms need a project name to carry out configuration.
        sd_command = f"{sd_command} --deployed-project-name my_blog_project"

    # Add --unit-testing argument to the call.
    sd_command = sd_command.replace("simple_deploy", "simple_deploy --unit-testing")

    # Get the path to the Python interpreter in the virtual environment.
    #   We'll use the full path to the interpreter, rather than trying to rely on
    #   an active venv.
    python_exe = Path(tmp_dir) / "b_env" / "bin" / "python"
    sd_command = sd_command.replace("python", str(python_exe))

    # Make the call to simple_deploy.
    #   The `text=True` argument causes this to return stdout and stderr as strings, not objects.
    sd_call = subprocess.Popen(split(sd_command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = sd_call.communicate()

    return stdout, stderr

def make_git_call(tmp_dir, git_call):
    """Make a git call against the test project.
    Returns:
    - stdout, stderr as strings.
    """
    os.chdir(tmp_dir)
    git_call_object = subprocess.Popen(split(git_call), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = git_call_object.communicate()

    return stdout, stderr