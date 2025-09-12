"""Manage deployment to a variety of platforms.

Configuration-only mode:
    $ python manage.py deploy
    Configures project for deployment to the specified platform.

Automated mode:
    $ python manage.py deploy --automate-all
    Configures project for deployment, *and* issues platform's CLI commands to create
    any resources needed for deployment. Also commits changes, and pushes project.

Overview:
    This is the command that's called to manage the configuration. In the automated
    mode, it also makes the actual deployment. The entire process is coordinated in
    handle():
    - Parse the CLI options that were passed.
    - Start logging, unless suppressed.
    - Validate the set of arguments that were passed.
    - Inspect the user's system.
    - Inspect the project.
    - Add django-simple-deploy to project requirements.
    - Call the plugin's `deploy()` method.

See the documentation for more about this process:
    https://django-simple-deploy.readthedocs.io/en/latest/
"""

import sys, os, platform, re, subprocess, logging, shlex
from datetime import datetime
from pathlib import Path
from importlib import import_module
from importlib.metadata import version

from django.core.management.base import BaseCommand
from django.conf import settings

import toml

from . import dsd_messages
from .utils import dsd_utils
from .utils import plugin_utils

from .utils.plugin_utils import dsd_config
from .utils.command_errors import DSDCommandError
from . import cli

from django_simple_deploy.plugins import pm


class Command(BaseCommand):
    """Configure a project for deployment to a specific platform.

    If using --automate-all, carry out the actual deployment as well.
    """

    # Show a summary of django-simple-deploy in the help text.
    help = "Configures your project for deployment to the specified platform."

    def __init__(self):
        """Customize help output, assign attributes."""

        # Keep default BaseCommand args out of help text.
        self.suppressed_base_arguments.update(
            [
                "--version",
                "-v",
                "--settings",
                "--pythonpath",
                "--traceback",
                "--no-color",
                "--force-color",
            ]
        )
        # Ensure that --skip-checks is not included in help output.
        self.requires_system_checks = []

        # Import the platform-specific plugin module. This performs some validation, so
        # it's best to call this before modifying project in any way. Also, the plugin
        # manager is needed in `add_arguments()`, so it needs to be defined here.
        platform_module = self._load_plugin()
        pm.register(platform_module)

        super().__init__()

    def create_parser(self, prog_name, subcommand, **kwargs):
        """Customize the ArgumentParser object that will be created."""
        epilog = "For more help, see the full documentation at: "
        epilog += "https://django-simple-deploy.readthedocs.io"
        parser = super().create_parser(
            prog_name,
            subcommand,
            usage=cli.get_usage(),
            epilog=epilog,
            add_help=False,
            **kwargs,
        )

        return parser

    def add_arguments(self, parser):
        """Define CLI options."""
        # Add core django-simple-deploy CLI args.
        sd_cli = cli.SimpleDeployCLI(parser)

        # Add plugin-specific CLI args.
        pm.hook.dsd_get_plugin_cli_args(parser=parser)

    def handle(self, *args, **options):
        """Manage the overall configuration process.

        Parse options, start logging, validate the deploy command used, inspect
        the user's system, inspect the project.
        Verify that the user should be able to deploy to this platform.
        Add django-simple-deploy to project requirements.
        Call the platform-specific deploy() method.
        """
        # Need to define stdout before the first call to write_output().
        dsd_config.stdout = self.stdout

        plugin_utils.write_output(
            "Configuring project for deployment...", skip_logging=True
        )

        # CLI options need to be parsed before logging starts, in case --no-logging
        # has been passed.
        self._parse_cli_options(options)

        if dsd_config.log_output:
            self._start_logging()
            self._log_cli_args(options)

        self._validate_command()

        # Get installed version.
        dsd_config.version = version("django-simple-deploy")

        # DEV: It may be reasonable to validate the plugin earlier.
        self._validate_plugin(pm)

        platform_name = self.plugin_config.platform_name
        plugin_utils.write_output(f"\nDeployment target: {platform_name}")
        plugin_utils.write_output(f"  Using plugin: {self.plugin_name}")

        # Inspect the user's system and project, and make sure django-simple-deploy is included
        # in project requirements.
        self._inspect_system()
        self._inspect_project()
        self._add_dsd_req()

        self._confirm_automate_all(pm)

        # At this point dsd_config is fully defined, so we can validate it before handing
        # responsibility off to plugin.
        dsd_config.validate()

        # Platform-agnostic work is finished. Hand off to plugin.
        pm.hook.dsd_deploy()

    def _parse_cli_options(self, options):
        """Parse CLI options from deploy command."""

        # Platform-agnostic arguments.
        dsd_config.automate_all = options["automate_all"]
        dsd_config.log_output = not (options["no_logging"])
        self.ignore_unclean_git = options["ignore_unclean_git"]

        # Platform.sh arguments.
        dsd_config.deployed_project_name = options["deployed_project_name"]
        dsd_config.region = options["region"]

        # Developer arguments.
        dsd_config.unit_testing = options["unit_testing"]
        dsd_config.e2e_testing = options["e2e_testing"]

    def _start_logging(self):
        """Set up for logging.

        Create a log directory if needed; create a new log file for every run of
        `deploy`. Since deploy should be called once, it's helpful to have
        separate files for each run. It should only be run more than once when users
        are fixing errors that are called out by deploy, or if a remote resource
        hangs.

        Log path is added to .gitignore when the project is inspected.
        See _inspect_project().

        Returns:
            None
        """
        created_log_dir = self._create_log_dir()

        # Instantiate a logger. Append a timestamp so each new run generates a unique
        # log filename.
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        log_filename = f"dsd_{timestamp}.log"
        verbose_log_path = self.log_dir_path / log_filename
        verbose_logger = logging.basicConfig(
            level=logging.INFO,
            filename=verbose_log_path,
            format="%(asctime)s %(levelname)s: %(message)s",
        )

        plugin_utils.write_output("Logging run of `manage.py deploy`...")
        plugin_utils.write_output(f"Created {verbose_log_path}.")

    def _log_cli_args(self, options):
        """Log the args used for this call."""
        plugin_utils.log_info(f"\nCLI args:")
        for option, value in options.items():
            plugin_utils.log_info(f"  {option}: {value}")

    def _create_log_dir(self):
        """Create a directory to hold log files, if not already present.

        Returns:
            bool: True if created directory, False if already one present.
        """
        # We're primarily calling Path() because wagtail still uses string paths!
        self.log_dir_path = Path(settings.BASE_DIR) / "dsd_logs"
        if not self.log_dir_path.exists():
            self.log_dir_path.mkdir()
            return True
        else:
            return False

    def _load_plugin(self):
        """Load the appropriate platform-specific plugin module for this deployment.

        The plugin name is not usually specified as a CLI arg, because most users will
        only have one plugin installed. We inspect the installed packages, and try to
        identify the installed plugin automatically.
        """
        self.plugin_name = dsd_utils.get_plugin_name()

        platform_module = import_module(f"{self.plugin_name}.deploy")
        return platform_module

    def _validate_command(self):
        """Verify deploy has been called with a valid set of arguments.

        Returns:
            None

        Raises:
            DSDCommandError: If we can't do a deployment with given set of args.
        """
        # DEV: This was used to validate the deprecated --platform arg, but will probably
        # be used again.
        pass

    def _inspect_system(self):
        """Inspect the user's local system for relevant information.

        Uses dsd_config.on_windows and dsd_config.on_macos because those are clean checks to run.
        May want to refactor to dsd_config.user_system at some point. Don't ever use
        dsd_config.platform, because "platform" usually refers to the host we're deploying to.

        Linux is not mentioned because so far, if it works on macOS it works on Linux.
        """
        dsd_config.use_shell = False
        dsd_config.on_windows, dsd_config.on_macos = False, False
        if platform.system() == "Windows":
            dsd_config.on_windows = True
            dsd_config.use_shell = True
            plugin_utils.log_info("Local platform identified: Windows")
        elif platform.system() == "Darwin":
            dsd_config.on_macos = True
            plugin_utils.log_info("Local platform identified: macOS")

    def _inspect_project(self):
        """Inspect the local project.

        Find out everything we need to know about the project before making any remote
        calls.
            Determine project name.
            Find paths: .git/, settings, project root.
            Determine if it's a nested project or not.
            Get the dependency management approach: requirements.txt, Pipenv, Poetry
            Get current requirements.

        Anything that might cause us to exit before making the first remote call should
        be inspected here.

        Sets:
            self.local_project_name, self.project_root, self.settings_path,
            self.pkg_manager, self.requirements

        Returns:
            None
        """
        dsd_config.local_project_name = settings.ROOT_URLCONF.replace(".urls", "")
        plugin_utils.log_info(f"Local project name: {dsd_config.local_project_name}")

        dsd_config.project_root = Path(settings.BASE_DIR)
        plugin_utils.log_info(f"Project root: {dsd_config.project_root}")

        # Find .git location, and make sure there's a clean status.
        self._find_git_dir()
        self._check_git_status()

        # Now that we know where .git is, we can ignore dsd logs.
        if dsd_config.log_output:
            self._ignore_sd_logs()

        dsd_config.settings_path = self._get_settings_path()

        # Find out which package manager is being used: req_txt, poetry, or pipenv
        dsd_config.pkg_manager = self._get_dep_man_approach()
        msg = f"Dependency management system: {dsd_config.pkg_manager}"
        plugin_utils.write_output(msg)

        dsd_config.requirements = self._get_current_requirements()

    def _find_git_dir(self):
        """Find .git/ location.

        Should be in BASE_DIR or BASE_DIR.parent. If it's in BASE_DIR.parent, this is a
        project with a nested directory structure. A nested project has the structure
        set up by:
           `django-admin startproject project_name`
        A non-nested project has manage.py at the root level, started by:
           `django-admin startproject .`
        This matters for knowing where manage.py is, and knowing where the .git/ dir is
        likely to be.

        Sets:
            dsd_config.git_path, dsd_config.nested_project

        Returns:
            None

        Raises:
            DSDCommandError: If .git/ dir not found.
        """
        if (dsd_config.project_root / ".git").exists():
            dsd_config.git_path = dsd_config.project_root
            plugin_utils.write_output(f"Found .git dir at {dsd_config.git_path}.")
            dsd_config.nested_project = False
        elif (dsd_config.project_root.parent / ".git").exists():
            dsd_config.git_path = dsd_config.project_root.parent
            plugin_utils.write_output(f"Found .git dir at {dsd_config.git_path}.")
            dsd_config.nested_project = True
        else:
            error_msg = "Could not find a .git/ directory."
            error_msg += f"\n  Looked in {dsd_config.project_root} and in {dsd_config.project_root.parent}."
            raise DSDCommandError(error_msg)

    def _check_git_status(self):
        """Make sure all non-dsd changes have already been committed.

        All configuration-specific work should be contained in a single commit. This
        allows users to easily revert back to the version of the project that worked
        locally, if the overall deployment effort fails, or if they don't like what
        django-simple-deploy does for any reason.

        Don't just look for a clean git status. Some uncommitted changes related to
        django-simple-deploy's work is acceptable, for example if they are doing a couple
        runs to get things right.

        Users can override this check with the --ignore-unclean-git flag.

        Returns:
            None: If status is such that `deploy` can continue.

        Raises:
            DSDCommandError: If any reason found not to continue.
        """
        if self.ignore_unclean_git:
            msg = "Ignoring git status."
            plugin_utils.write_output(msg)
            return

        cmd = "git status --porcelain"
        output_obj = plugin_utils.run_quick_command(cmd)
        status_output = output_obj.stdout.decode()
        plugin_utils.log_info(f"{status_output}")

        cmd = "git diff --unified=0"
        output_obj = plugin_utils.run_quick_command(cmd)
        diff_output = output_obj.stdout.decode()
        plugin_utils.log_info(f"{diff_output}\n")

        proceed = dsd_utils.check_status_output(status_output, diff_output)

        if proceed:
            msg = "No uncommitted changes, other than django-simple-deploy work."
            plugin_utils.write_output(msg)
        else:
            self._raise_unclean_error()

    def _raise_unclean_error(self):
        """Raise unclean git status error."""
        error_msg = dsd_messages.unclean_git_status
        if dsd_config.automate_all:
            error_msg += dsd_messages.unclean_git_automate_all

        raise DSDCommandError(error_msg)

    def _ignore_sd_logs(self):
        """Add log dir to .gitignore.

        Adds a .gitignore file if one is not found.
        """
        ignore_msg = "dsd_logs/\n"

        gitignore_path = dsd_config.git_path / ".gitignore"
        if not gitignore_path.exists():
            # Make the .gitignore file, and add log directory.
            gitignore_path.write_text(ignore_msg, encoding="utf-8")
            plugin_utils.write_output("No .gitignore file found; created .gitignore.")
            plugin_utils.write_output("Added dsd_logs/ to .gitignore.")
        else:
            # Append log directory to .gitignore if it's not already there.
            contents = gitignore_path.read_text()
            if "dsd_logs/" not in contents:
                contents += f"\n{ignore_msg}"
                gitignore_path.write_text(contents)
                plugin_utils.write_output("Added dsd_logs/ to .gitignore")

    def _get_settings_path(self):
        """Find the settings file that we should modify.

        This is usually project_name/settings.py.
        For Wagtail and projects with a similar structure, this will be
          project_name/settings/production.py.
        """
        standard_path = dsd_config.project_root / dsd_config.local_project_name / "settings.py"
        if standard_path.exists():
            return standard_path

        wagtail_path = dsd_config.project_root / dsd_config.local_project_name / "settings" / "production.py"
        if wagtail_path.exists():
            return wagtail_path

        # Can't identify a settings path, so we need to bail.
        error_msg = f"Couldn't find a settings file. Tried {standard_path.as_posix()} and {wagtail_path.as_posix()}"
        raise DSDCommandError(error_msg)

    def _get_dep_man_approach(self):
        """Identify which dependency management approach the project uses.

        Looks for most specific tests first: Pipenv, Poetry, then requirements.txt. For
        example, if a project uses Poetry and has a requirements.txt file, we'll
        prioritize Poetry.

        Sets:
            self.pkg_manager

        Returns:
            str: "req_txt" | "poetry" | "pipenv"

        Raises:
            DSDCommandError: If a pkg manager can't be identified.
        """
        if (dsd_config.git_path / "Pipfile").exists():
            return "pipenv"
        elif self._check_using_poetry():
            return "poetry"
        elif (dsd_config.git_path / "requirements.txt").exists():
            return "req_txt"

        # Exit if we haven't found any requirements.
        error_msg = (
            f"Couldn't find any specified requirements in {dsd_config.git_path}."
        )
        raise DSDCommandError(error_msg)

    def _check_using_poetry(self):
        """Check if the project appears to be using poetry.

        Check for a pyproject.toml file with a [tool.poetry] section.

        Returns:
            bool: True if found, False if not found.
        """
        path = dsd_config.git_path / "pyproject.toml"
        if not path.exists():
            return False

        pptoml_data = toml.load(path)
        return "poetry" in pptoml_data.get("tool", {})

    def _get_current_requirements(self):
        """Get current project requirements.

        We need to know which requirements are already specified, so we can add any that
        are needed on the remote platform. We don't need to deal with version numbers
        for most packages.

        Sets:
            self.req_txt_path

        Returns:
            List[str]: List of strings, each representing a requirement.
        """
        msg = "Checking current project requirements..."
        plugin_utils.write_output(msg)

        if dsd_config.pkg_manager == "req_txt":
            dsd_config.req_txt_path = dsd_config.git_path / "requirements.txt"
            requirements = dsd_utils.parse_req_txt(dsd_config.req_txt_path)
        elif dsd_config.pkg_manager == "pipenv":
            dsd_config.pipfile_path = dsd_config.git_path / "Pipfile"
            requirements = dsd_utils.parse_pipfile(dsd_config.pipfile_path)
        elif dsd_config.pkg_manager == "poetry":
            dsd_config.pyprojecttoml_path = dsd_config.git_path / "pyproject.toml"
            requirements = dsd_utils.parse_pyproject_toml(dsd_config.pyprojecttoml_path)

        # Report findings.
        msg = "  Found existing dependencies:"
        plugin_utils.write_output(msg)
        for requirement in requirements:
            msg = f"    {requirement}"
            plugin_utils.write_output(msg)

        return requirements

    def _add_dsd_req(self):
        """Add django-simple-deploy to the project's requirements.

        Since django_simple_deploy is in INSTALLED_APPS, it needs to be in the project's
        requirements. If it's missing, platforms will reject the push.
        """
        msg = "\nLooking for django-simple-deploy in requirements..."
        plugin_utils.write_output(msg)
        version_string = f"=={dsd_config.version}"
        plugin_utils.add_package("django-simple-deploy", version=version_string)

    def _validate_plugin(self, pm):
        """Check that all required hooks are implemented by plugin.

        Also, load and validate plugin config object.

        Returns:
            None
        Raises:
            DSDCommandError: If plugin found invalid in any way.
        """
        plugin = pm.list_name_plugin()[0][1]

        callers = [caller.name for caller in pm.get_hookcallers(plugin)]
        required_hooks = [
            "dsd_get_plugin_config",
        ]
        for hook in required_hooks:
            if hook not in callers:
                msg = f"\nPlugin missing required hook implementation: {hook}()"
                raise DSDCommandError(msg)

        # Load plugin config, and validate config.
        self.plugin_config = pm.hook.dsd_get_plugin_config()[0]

        # Make sure there's a confirmation msg for automate_all if needed.
        if self.plugin_config.automate_all_supported and dsd_config.automate_all:
            if not hasattr(self.plugin_config, "confirm_automate_all_msg"):
                msg = "\nThis plugin supports --automate-all, but does not provide a confirmation message."
                raise DSDCommandError(msg)

    def _confirm_automate_all(self, pm):
        """Confirm the user understands what --automate-all does.

        Also confirm that the selected plugin supports fully automated deployments.

        If confirmation not granted, exit with a message, but no error.
        """
        # Placing this check here keeps the handle() method cleaner.
        if not dsd_config.automate_all:
            return

        # Make sure this plugin supports automate-all.
        if not self.plugin_config.automate_all_supported:
            msg = "\nThis plugin does not support automated deployments."
            msg += "\nYou may want to try again without the --automate-all flag."
            raise DSDCommandError(msg)

        # Confirm the user wants to automate all steps.
        msg = self.plugin_config.confirm_automate_all_msg
        plugin_utils.write_output(msg)
        confirmed = plugin_utils.get_confirmation()

        if confirmed:
            plugin_utils.write_output("Automating all steps...")
        else:
            # Quit with a message, but don't raise an error.
            plugin_utils.write_output(dsd_messages.cancel_automate_all)
            sys.exit()
