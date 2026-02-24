"""Helper functions for e2e tests of different platforms.

The functions in this module are not specific to any one platform. If a function
  starts to be used by tests for more than one platform, it should be moved here.
"""

import subprocess, shlex, sys, time, os, signal
from pathlib import Path
from textwrap import dedent


def make_sp_call(cmd, capture_output=False):
    """Make a subprocess call.

    This wrapper function lets test code use full commands, rather than
      lists of command parts. This makes it much easier to follow what testing
      code is doing.

    Returns: None, or CompletedProcess instance.
    """
    cmd_parts = shlex.split(cmd)

    if os.name == "nt":
        # On Windows, only git commands need to be split?
        if "git" in cmd:
            return subprocess.run(cmd_parts, capture_output=capture_output)
        elif "heroku" in cmd:
            # Doesn't find the heroku command without shell=True.
            return subprocess.run(cmd, capture_output=capture_output, shell=True)
        else:
            return subprocess.run(cmd, capture_output=capture_output)
    else:
        return subprocess.run(cmd_parts, capture_output=capture_output)


def get_python_exe(tmp_project):
    """Get the path to the Python interpreter in the virtual environment.

    We'll use the full path to the interpreter, rather than trying to rely on
    an active venv.
    """
    if sys.platform == "win32":
        python_exe = Path(tmp_project) / "b_env" / "Scripts" / "python.exe"
    else:
        python_exe = Path(tmp_project) / "b_env" / "bin" / "python"

    return python_exe.as_posix()


def run_simple_deploy(python_cmd, platform="", automate_all=False, plugin_args_string=""):
    """Run deploy against the test project."""
    print("Running manage.py deploy...")
    if automate_all:
        make_sp_call(f"{python_cmd} manage.py deploy --automate-all --e2e-testing {plugin_args_string}")
    else:
        make_sp_call(f"{python_cmd} manage.py deploy --e2e-testing {plugin_args_string} ")


def commit_configuration_changes():
    """Commit configuration changes made by dsd."""
    print("\n\nCommitting changes...")
    make_sp_call("git add .")
    make_sp_call("git commit -am 'Configured for deployment.'")


def check_deployed_app_functionality(python_cmd, url):
    """Test functionality of the deployed app.
    Note: Can't call this function test_ because pytest will try to run it directly.
    """
    # Pause before testing functionality, otherwise app may not yet be available.
    time.sleep(10)

    print("\n  Testing functionality of deployed app...")

    test_output = make_sp_call(
        f"{python_cmd} test_deployed_app_functionality.py --url {url}",
        capture_output=True,
    ).stdout.decode()

    print(test_output)
    print("    Finished testing functionality of deployed project.")
    breakpoint()

    return "--- All tested functionality works. ---" in test_output


def check_local_app_functionality(python_cmd):
    """Verify that local project still functions.
    Note: Can't call this function test_ because pytest will try to run it directly."""
    print("\n  Testing local functionality with runserver...")
    make_sp_call(f"{python_cmd} manage.py migrate")

    # Start the runserver process.
    # On Linux, runserver will spawn child processes, which need to be handled as a group.
    if sys.platform == "linux":
        run_server = subprocess.Popen(
            f"{python_cmd} manage.py runserver 8008", shell=True, preexec_fn=os.setpgrp
        )
    elif sys.platform=="win32":
        cmd = f"{python_cmd} manage.py runserver 8008 --noreload"
        cmd_parts = shlex.split(cmd)
        run_server = subprocess.Popen(
            cmd_parts,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )
    else:
        run_server = subprocess.Popen(
            f"{python_cmd} manage.py runserver 8008", shell=True
        )

    time.sleep(1)

    # Test the local project using the runserver process.
    test_output = make_sp_call(
        f"{python_cmd} test_deployed_app_functionality.py --url http://localhost:8008/",
        capture_output=True,
    ).stdout.decode()

    # Kill the runserver process.
    if sys.platform == "linux":
        os.killpg(run_server.pid, signal.SIGKILL)
    elif sys.platform == "win32":
        run_server.send_signal(signal.CTRL_BREAK_EVENT)
    else:
        run_server.terminate()

    print(test_output)
    print("    Finished testing local functionality.")

    return "--- All tested functionality works. ---" in test_output


def summarize_results(
    remote_functionality_passed, local_functionality_passed, cli_options, tmp_proj_dir
):
    """Summarize test results.
    pytest's summary is not particularly helpful here.
    """

    if remote_functionality_passed:
        msg_remote = dedent("The deployment was successful.")
    else:
        msg_remote = dedent(
            """Some or all of the remote functionality tests failed.
            
        You may want to refresh the browser page, and see if
          the deployment just took longer than usual.
        """
        )

    if local_functionality_passed:
        msg_local = dedent("The project still works locally.")
    else:
        msg_local = dedent("The deployment process has impacted local functionality.")

    msg = dedent(
        f"""
        ************************************
        ***** e2e test summary *****

        Temp project dir: {tmp_proj_dir}

        Test options:
        - Tested {'PyPI' if cli_options.pypi else 'local'} version of django-simple-deploy.
        - Plugin: {cli_options.plugin_name}
        - Package manager: {cli_options.pkg_manager}
        - {'Used' if cli_options.automate_all else 'Did not use'} `--automate-all` flag.

        {msg_remote}
        {msg_local}

        *****     End test summary     *****
        ************************************

    """
    )
    print(msg)


def confirm_destroy_project(cli_options):
    """Confirm that we should destroy the deployed project."""
    if cli_options.skip_confirmations:
        return True

    while True:
        confirmation = input("Destroy remote project? ")

        if confirmation.lower() in ["y", "yes"]:
            print("Okay, tearing down...")
            return True

        if confirmation.lower() in ["n", "no"]:
            print("Okay, leaving project deployed.")
            return False

        print("Please answer yes or no.")
