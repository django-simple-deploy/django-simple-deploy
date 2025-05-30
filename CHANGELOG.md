Changelog: django-simple-deploy
===

For inspiration and motivation, see [Keep a CHANGELOG](https://keepachangelog.com/en/0.3.0/).

1.0 - Stable release
---

This release will have a stable public interface for end users, and for plugin developers as well. The project will continue to be refined internally and may gain some new features, but will have overall stability as a high priority.

### (Unreleased)

#### External changes

- Added docs/announcements section, with 1.0 release announcement.

#### Internal changes

- Update docs/requirements.txt, and readthedocs.yml to fix issue when building docs.


### 1.0.0 - Stable release

#### External changes

- Updated main image and name of log directory in main README.
- Updated roadmap for post-1.0 phase of development.

#### Internal changes

- Uses a cross-platform approach to identifying which plugin is being tested.
- Added windows-compatible dependencies to vendor/ for integration tests. All tests pass on Windows.
- Updated core tests for Linux as well.
- Implements CI testing for Python 3.12 on macOS, Linux, and Windows.
- Updated requirements.txt, for dev work.
- Run CI testing on direct push to main.
- Add dependabot config.
  - Daily for main requirements.
  - Monthly for sample_project and tests/, until tests refactored to pull version from sample_project/.


0.9 - Simplified usage
---

### 0.9.4

#### External changes

- When adding `django-simple-deploy` as a dependency of the user's project, specifies the currently-installed version of `django-simple-deploy`. This makes sure the version installed on the host platform matches the version the user has installed locally. This makes testing more reliable, and should be the behavior that users would expect.

#### Internal changes

- `plugin_utils.check_reference_file()` accepts an absolute path to a reference file, and a context dictionary for dynamic reference files.
- Provides a fixture, `dsd_version`, for getting the version of `django-simple-deploy` that's being used during testing.

### 0.9.3

#### External changes

- Better documentation of `plugin_utils` and `dsd_config`.
- Main app renamed, from `simple_deploy` to `django_simple_deploy`. The app name now matches the package name. There is only the name `django-simple-deploy` its variant `django_simple_deploy`, and the `deploy` command. There should no longer be any reference to `simple_deploy`, which was sometimes used as an actual name and sometimes as shorthand for the overall project.
- Reviewed all public-facing messages and documentation for current usage.
- Removed most references to "pre-1.0" state.
- New doc page listing all known available plugins.

#### Internal changes

- Update many names to better reflect current state of the project, and remove historical baggage. Also, use some abbreviations such as `dsd_logs/` instead of `django_simple_deploy_logs/`.

### 0.9.2

#### External changes

- Documentation for `plugin_utils.py` and `sd_config.py`.

#### Internal changes

- New plugin utility function, `get_user_info()`. Useful for prompting the user for information such as a deployed project name.
- New plugin utility function, `read_log()`, for getting contents of the simple deploy log for the current run.
- Simpler and more effective approach to resetting the test project during integration testing.
- Uses `mkdocstrings-python` for auto-inclusion of some docstrings and source in documentation, ie for `plugin_utils.py` and `sd_config.py`.

### 0.9.1

#### External changes

- Updated README to reflect current usage.

#### Internal changes

- Gets a `plugin_conf` object from the plugin, instead of several individual attributes. This is much simpler and more future-proof.


### 0.9.0

#### External changes

- Command changed to `manage.py deploy` instead of `manage.py simple_deploy`.
- The `--platform` CLI arg is no longer needed. (It's removed, because the plugin makes it completely unnecessary.)
- Docs updated, new section focusing on plugins.

#### Internal changes

- Core gets target platform name from plugin.
- Auto-detects installed plugin.
- Option `--skip-plugin-tests` added, to run only core tests.
- Started general `tests/utils` utilities.
- Script in `developer_resources/` to update requirements for sample project.
- Functionality test updated to support static file names that include hashes.

0.8 - External plugins
---

### 0.8.1

#### External changes

- New tagline: "Deployment, for Djangonauts with deadlines."
- Updated all virtual environment names in docs from `dsd_env` to `.venv`.
- Brief update for docs to reflect installation workflow requiring user to specify a plugin.
- Updated docs for setting up a development environment, and testing the project.

#### Internal changes

- Moved all info in setup.cfg to pyproject.toml.
- Set and tested minimum versions for top-level dependencies.

### 0.8.0

#### External changes

- Requires default plugins: dsd-flyio, dsd-platformsh, dsd-heroku.
- Updated quick start docs for Heroku, replacing deprecated `mini` Postgres instance with `essential-0`.

#### Internal changes

- All platform-specific code has been moved to external plugins.
  - Selects appropriate plugin based on `--platform` arg, and names of plugins that have been installed.
  - Plugin naming convention: `dsd-<platformname>-<extension>`.
  - Underscores in `--platform` arg are ignored when selecting plugin to use. For example, `--platform fly_io` will select a plugin named `dsd-flyio-<extension>`.
- When running `pytest`, installed plugins are auto-discovered and their unit and integration tests are run.
- When running end to end tests, use `--plugin dsd_flyio` instead of `--platform fly_io`. The platform arg will be inferred from the plugin name, allowing you to run tests for any default or third-party plugin.

0.7 - Internal plugin model
---

The goal for the 0.7 series is to support an internal plugin model. There shouldn't be many external changes due to this model, but this is an important enough step towards a 1.0 release that it warrants a bump in the minor version number. The 0.8.0 release should indicate preliminary support for external plugins.

### 0.7.3

#### External changes

- None

#### Internal changes

- Adds several utility functions for use by platform-specific plugins: `add_file()`, `add_dir()`, `modify_file()`, and `get_template_string()`. Each of the three platforms use these functions where appropriate. Reorganizes `utils.py` into `utils/sd_utils.py` and `utils/plugin_utils.py`.
- Accesses platform messages directly, rather than through an attribute.
- Simpler access to `sd_utils`.
- Renamed `deploy_messages` -> `sd_messages`.
- Moved `SimpleDeployCommandError` to `plugin_utils`.
- Move all functions that platform plugins use to `plugin_utils`, and out of `Command`.
- Created `SDConfig` class to store all information that a plugin might need to access. This avoids having to pass around an instance of `Command`, which had grown pretty awkward.
- `SDConfig` instance is now a global in `plugin_utils`. Despite the oft-repeated advice not to use globals, it really seems to make sense in this context. It simplifies most plugin utility function signatures. For example: `plugin_utils.write_output(self.sd_config, msg)` is now `plugin_utils.write_output(msg)`. There are numerous ways to protect the config instance if the need arises, or choose a different non-globabl approach with this as a better starting point.
- `SDConfig.validate()` checks that attributes required by all plugins have been set.
- Plugins import `sd_config` directly. This simplifies the use of `sd_config` significantly in plugins. For example, `self.sd_config.automate_all` becomes `sd_config.automate_all`. Also, core no longer needs to pass anything off directly to plugins.
- `SDConfig` is instantiated once, at the module level, in `plugin_utils`. It's imported directly into simple_deploy.py and each plugin's `platform_deployer` module. Attributes are set by `Command`, and read by plugins as needed.
- `SimpleDeployCommandError` is moved to its own module, and imported directly into any module that needs it.


### 0.7.2

#### External changes

- On Fly and Heroku, append to `STATICFILES_DIRS` if it already exists, rather than overwriting the existing setting.

### 0.7.1

#### External changes

- Fly.io deployer gets permission before overwriting `Dockerfile`.

#### Internal changes

- All platform-specific tests moved to plugin directories.
- Integration and e2e tests use `uv` for setup work, when available as a system command.
- Ran Black against the entire repository.
- Platform deployers have access to cross-platform `sd.messages`.
- Added two messages to `sd`:
    - `file_found(filename)`: Found an existing file, that we need permission to replace.
    - `file_replace_rejected(filename)`: User does not grant permission to replace file.
- Started testing dynamic cross-platform messages.


### 0.7.0

#### External changes

- Requires `pluggy`.
- Fixes bug in validating authenticated Heroku CLI session.

#### Internal changes

- All platforms use a plugin model internally.
- Developer resources moved to platform-specific subdirs.
- All imports in plugins are relative to the plugin, rather than using simple_deploy paths.
- Simpler implementation of `write_file_from_template()` utility function.
- `PlatformDeployer` class moved to separate file for all plugins.
- Core simple_deploy verifies that selected plugin implements required hooks.
    - All plugins must implement `simple_deploy_automate_all_supported()`, which returns a boolean indicating whether the plugin supports the `--automate-all` flag. If `--automate-all` is supported, the plugin must also implement `simple_deploy_get_automate_all_msg()`, which provides a platform-specific message for confirming the usage of `--automate-all`.
    - All plugins must implement `simple_deploy_deploy()`.

0.6 - Stable deployments on all three platforms
---

### 0.6.5

#### External changes

- Platform.sh deployments work with project names including spaces and capital letters. These names are converted to lowercase with underscores during configuration.

### 0.6.4

#### External changes

- Platform.sh now works for users with multiple orgs, and multiple projects already deployed.
- Removed warnings about preliminary status of Fly.io and Platform.sh.

#### Internal changes

### 0.6.3

#### External changes

- Platform.sh deployments were broken. Fixed redundant, broken check for confirming automate_all.

#### Internal changes

- Move stale issues and tasks to [Parking Lot](https://django-simple-deploy.readthedocs.io/en/latest/contributing/parking_lot/).
- Consistent approach to managing settings and env vars across all platforms.

### 0.6.2

Many changes to update the project and work toward a plugin-based model. Most of this work is around simplifying workflows, and making them consistent across platforms.

#### External changes

- Fly deployment works for multiple deployments.
    - Previously, Fly deployments would fail if you already had a project deployed to Fly, because it wasn't clear which resources to use for the current deployment.
    - Now, if it's not obvious which resources to use, user is presented with a numbered list of resources so they can choose the appropriate one.
- Heroku configuration updated to match current process in Heroku docs.
    - Use Heroku Postgres `essential-0` instead of deprecated `mini`.
    - Update database configuration, and static file configuration.

#### Internal changes

- Refactor deploy scripts for all three platforms.
- Restructure tests to make a clear distinction between unit, integration, and end-to-end tests.
- Use numbered choices to let user select appropriate remote resources when not obvious which one to use.
- More small utility functions, with better unit tests.
- More specific CLI calls for each platform, to make parsing output easier. For example, use `--json` flags whenever they're available.
- Docstrings are more consistent.
- Started Coding Guide and Architecture Notes. Started documenting the contract between host and plugins.
- Core simple_deploy.py confirms `--automate-all` usage, using platform-specific confirmation message.
- Simpler approach to managing settings. Write as a block, and get permission to overwrite if existing platform-specific settings block found in settings.py (Heroku).
- Sample project updated to use POST-based logout.

### 0.6.1

#### External changes

- Fixes some issues managing Fly and Platform.sh CLI usage on Ubuntu and macOS.

### 0.6.0

Deployments should work on all three platforms, for all major OSes. Any fixes from this point should be much more minor bugfixes, rather than rethinking the overall approach. This should be a transition to 1.0.

#### External changes

- Detects missing Heroku CLI on Ubuntu.
- Creates a Postgres database on Heroku as needed.
- Updates roadmap.

#### Internal changes

- Starts to use `--json` on some Heroku CLI calls.


0.5 - Supporting Fly.io, Platform.sh, and Heroku
---

### 0.5.18

Stabilize deployments to Fly.io. Previously, deployment to Fly.io would fail if you already had an app deployed on Fly. This release addresses that issue, and significantly improves the process for deploying to Fly.

#### External changes

- Shows all the user's undeployed apps on Fly.io, and gets confirmation that the correct app to deploy to has been chosen.
- If a database is found with a name matching the selected app, gets confirmation that it's okay to use that database.
- Updates all messages related to Fly.io deployments.

#### Internal changes

- Updated readthedocs config file.
- Fly `deploy.py` file is longer, and needs some refactoring.


### 0.5.17

Improve logging to include all project inspection steps. This should help with development and troubleshooting.

#### External changes

- Logs all system and project inspection steps.

#### Internal changes

- Creates log file immediately, unless `--skip-logging` is used. Previously, a log file wasn't written until we were writing other changes to the project.
- Implements `SimpleDeployCommandError`, which logs the error before raising `CommandError`. `CommandError` should not be used, unless the error output contains sensitive information.
- Implements `log_info()` method, which only logs information without writing it to the console.


### 0.5.16

Deployment to Platform.sh should be stable. Resumes preliminary support for Fly.io. Heroku deployment is probably broken for new users.

#### External changes

- Updates to documentation:
    - Updated information in Choosing a Platform.
    - Many smaller documentation improvements from multiple people looking closely at docs.
    - Started official documentation for integration tests.
- Fly.io:
    - Assumes you have no existing Fly apps.
    - Identifies lowest-latency region to deploy to; defaults to 'sea' if that information is unattainable.
    - Deprecate use of `flyctl`; use `fly` consistently throughout.
- Heroku:
    - Uses `'*'` for `ALLOWED_HOSTS` on Heroku, as a temp fix.

#### Internal changes

- Added `.venv` to `.gitignore`, so developers don't have to use `dsd_env`.
- Unit tests:
    - No longer use shell scripts;
    - Check for Poetry and Pipenv before running;
    - No longer require any platform's CLI to be installed;
    - Fixed `rum` misspelling of `rm` in unit tests using Poetry, which should improve accuracy of unit testing when using Poetry.
    - Pass on Windows as well as macOS and Linux.
    - Add `simple_deploy` to Poetry and Pipenv requirements for fly configurations.
- Integration tests
    - Converts most existing functionality in integration tests from shell scripts that only work on macOS/ Linux, to cross-platform functionality.
    - Prints summary of functionality tests.
- Other changes
    - Validates pytest call, to run either unit tests or integration tests, not both. Also require `-s` for integration tests.
    - New tool for standing up a dev environment: `build_dev_env.py`
    - Started less formal notes about each platform, in *developer_resources/*.
    - On Fly deployments, updates `fly open` calls to `fly apps open -a <app-name>`. Also updates deprecated `fly regions list -a` to get region with lowest latency.


### 0.5.15

#### External changes

- Heroku deployments work again.

#### Internal changes

- Integration test runs `pip cache purge` before installing simple deploy when using `-t pypi` flag.
    - This flag is often used immediately after making a new release, and this should ensure the new version is installed from PyPI.
- Calling `pytest` from project root generates a clean, simple reminder to cd to `unit_tests/` first.
- The version of `psycopg2` no longer needs to be pinned to `<2.9` on Heroku deployments using requirements.txt.


### 0.5.14

#### External changes

- Clarified documentation about configuration-only mode. We do sometimes create remote resources on the user's behalf, but only when we can't easily ask users to do so before running `simple_deploy`.
- All three platforms now support all three dependency management systems (bare `requirements.txt` file, Poetry, and Pipenv).
- Updated documentation about unit tests.
- Official documentation includes a roadmap, with a focus on reaching a 1.0 release.

#### Internal changes

- Started platform-agnostic tests for the process of inspecting local projects.
- The check for whether Poetry is being used is more specific.
- Every unit test now runs once for each dependency management system.
- The dependency management system is identified in `simple_deploy.py`, but platform-specific scripts make all decisions about what to do with that information.
    - Better internal support for platforms to work with requirements. There's a simple `add_package()` method in `simple_deploy.py`, as well as `add_packages()`. These then call the appropriate method for the current dependency management system in use.
    - Docker-based platforms make appropriate use of specific package managers, ie creating an optional `deploy` group in `pyproject.toml` when Poetry is being used.

### 0.5.13

#### External changes

- The output of `manage.py simple_deploy --help` is significantly improved.
- CLI-related error messages have been improved.
- The CLI is thoroughly documented on RtD.


#### Internal changes

- Moved all platform-specific files to their own directory. The only reference to a specific platform in *simple_deploy.py* is now the validation of the platform name.
    - Simplified *setup.cfg* to only refer to the `simple_deploy` package.
    - Simplified use of the Django template engine to write and modify files for configuration; see `write_file_from_template()` in *utils.py*.
    - Platform-specific imports are now done dynamically in *simple_deploy.py*, so only the files for the targeted platform are actually imported.
- Implementation of the CLI has been improved:
    - All CLI args are now defined in a separate module, `cli.py`.
    - Help output is covered in a unit test.
- Other developer-focused documentation improvements:    
    - Documented maintenance of docs.
    - Started ADR documentation.
    - Added Black to requirements, and used it to format the new `cli.py` file.

### 0.5.12

#### External changes:
- Removes local dependence on `platformshconfig`. Uses `os.environ.get()` locally to check whether deployment-specific settings should be used.

### 0.5.11

#### External changes:
- Fixed validation of `--platform` argument when used with `--automate-all`.

#### Internal changes:
- Removed `execute_subp_run_parts()`, and using `shlex.split(cmd)` instead of `cmd.split()`.

### 0.5.10

- Streams output of `platform create` when deploying to Platform.sh using `--automate-all`. This makes it more clear that the deployment has not hung on the `create` step.

### 0.5.9

- When configuring for Fly.io deployments, uses whitenoise to serve static files. Runs collectstatic during the build process.

### 0.5.8

- Updated unit test suite.
    - Unit test runs add `simple_deploy` to `INSTALLED_APPS` after last commit, like most end users would.
    - Unit tests are reorganized to separate tests for each platform, and to have a dedicated set of platform-agnostic tests.
    - Most shell scripts have been moved to a `utils/` directory.
    - A much simpler approach to testing invalid CLI calls is used.
    - Includes a basic set of unit tests for Fly.io configuration .
    - Each `unit_tests/platforms/` dir contains a `reference_files` directory. When unit tests run, modified sample project files are compared to these reference files. This makes it much easier to reason about unit tests, and provides a nice set of files to see exactly what changes `simple_deploy` makes to the sample project's files.
    - The sample project is only built once for every test session, rather than once per test module. The test project is reset for each new test module. This results in a speedup from ~52s to ~16s for the entire suite at this point. More importantly, testing more platforms and dependency management approaches will only incrementally increase test duration, rather than multiplying test duration.
    - Official documentation covers how to run unit tests. This update also includes some minor but important updates to the unit tests. These updates center around a better use of `autouse=True` where appropriate, and better use and explanation of scope.
    - In unit tests, we make sure the main branch is named `main`. Some tests expect to see references to the `main` branch in CLI output, and this would have failed on any contributor or CI system with a different default branch name.
- Configuration works when the target project's `settings.BASE_DIR` is a string. This affects any project whose setting file was generated in Django 3.0 or earlier, and hasn't been updated to use `Path` objects.
- When configuring for Heroku deployments, Whitenoise is added to middleware. This fixes a bug where the admin site on Heroku deployments does not have access to static resources such as css and js.

### 0.5.7

- Started the Contributing section on the official documentation:
  - Main contributing page
  - Documenting a Test Run
  - Testing on Your Own Account
  - Setting up a Development Environment
- Added issue template for documenting test runs. 
- Deployments on Platform.sh no longer include a `.platform/routes.yaml` file. 

### 0.5.6

- Documentation for managing PRs and releases moved to Read the Docs.
- Documentation includes installing `platformshconfig` when deploying to Platform.sh.
- Removes auto-update block from `.platform.app.yaml`.
- Integration tests check that running simple_deploy does not affect local functionality using `runserver`.
    - Update configuration for Fly.io and Platform.sh to not interfere with local functionality using `runserver`.
- Updated sample blog project to Django 4.1.2.
    - Modified `test_deployed_app_functionality.py` to not require a trailing forward slash.
    - Added notes about the differences between nested and non-nested projects.
- Deployments to Fly.io use the deployed project name in `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` settings.

### 0.5.5

- Streams output of `platform push`.

### 0.5.4

- Streams output of long-running commands `fly postgres create` and `fly deploy`. This makes it much easier to know that the deployment is continuing, rather than hanging.

### 0.5.3

- Generates a `.dockerignore` file when deploying to Fly.io.

### 0.5.2

- Uses [updated Dockerfile](https://github.com/superfly/flyctl/pull/1366) from Fly.io.
- The `-y` flag skips confirmation for teardown when running integration tests.

### 0.5.1

- Official documentation moved to [Read the Docs](https://django-simple-deploy.readthedocs.io/en/latest/).
    - Quick-start guides for all three supported platforms.
- Better check of `git status` when running `simple_deploy`. If the only uncommitted change is adding `simple_deploy` to `INSTALLED_APPS`, no error is raised.

### 0.5.0

- Preliminary support for Fly.io
    - Configuration-only and `--automate-all` approaches work on my macOS.
    - Probably only works when you don't have any other Fly.io projects deployed.
    - No documentation for Fly.io yet.
    - No unit tests yet.
    - Integration tests work.

0.4 - Supporting Heroku & Platform.sh
---

### 0.4.3

- Refining support of Platform.sh:
    - Initial unit tests for Platform.sh.
    - Initial integration tests written for Platform.sh.
    - `DEBUG = False` by default on Platform.sh.
    - Check that `platform create` has been run, or that a deployed project name has been provided.
    - More informative error messages if any prerequisite conditions are not met, such as running `platform create`.
    - `--automate-all` now works on Platform.sh.
    - Improved success messages after configuration-only run.
- Significant restructuring of simple_deploy's architecture, to more cleanly separate platform-agnostic work from platform-specific work. For example, see [Issue 89](https://github.com/ehmatthes/django-simple-deploy/issues/89).
- More integrity checks before making any configuration changes:
    - Check `git status` before beginning configuration work. Warn users and exit if status is not `working tree clean`. The `--ignore-unclean-git` flag will override this warning.
    - Check that Platform.sh CLI or Heroku CLI are installed before configuring for those platforms.
- Developer-focused improvements:
    - Added a `-y` flag to integration test script, to skip bash script confirmations.
    - Separated `--local-test` flag into `--unit-testing` and `--integration-testing` flags.

### 0.4.2

- Requires `--platform` flag.
    - There's no reason to have a default platform; deployment is a significant enough step that users should have a specific deployment target in mind. If the `--platform` flag is omitted, exit with a message displaying a list of platforms that are supported.

### 0.4.1

- Simplified MANIFEST.in
    - No user-facing changes, but built release to verify that changes don't break the release process.

### 0.4.0

- Removed support for Azure.
  - See detailed rationale in [Stop supporting Azure](https://github.com/ehmatthes/django-simple-deploy/issues/83).
  - Brief rationale: Focus django-simple-deploy on platforms like Heroku and Platform.sh where everything is contained in a single project, rather than a collection of services.
  - May resume support at some point in the future, but the project needs to evolve further before resuming this support.
  - Azure was used as a proof-of-concept to try supporting multiple platforms. Since then, I have had time to explore other platforms that are more suitable targets for django-simple-deploy.

0.3 - Supporting Heroku, Azure, & Platform.sh
---

### 0.3.0

- Preliminary support for platform.sh
    - If you have a platform.sh account, have installed the CLI, are using Git,
    and have a `requirements.txt` file, running
    `$ python manage.py simple_deploy --platform platform_sh`
    should configure your project for deployment on Platform.sh.
    - Then you'll need to commit changes, run `platform create`, and `platform push`.
    - Project should open with `platform url`.

0.2 - Supporting Heroku & Azure
---

### 0.2.5

- Fix image loading issue in main README on PyPI.

### 0.2.4

- Set up local unit testing (testing with no network calls).
- Moved all testing documentation to old_docs/.
- Simplified approach to the `ALLOWED_HOSTS` setting for Heroku deployments.
    - If the Heroku host is not found, append the Heroku host to `ALLOWED_HOSTS` in the Heroku-specific settings section, regardless of what else is in `ALLOWED_HOSTS`. This is motivated by reports from users who have followed tutorials that advise them to modify `ALLOWED_HOSTS` in a variety of ways. Appending our host in a Heroku-specific settings section should not cause any foreseeable problems.
    - Also improved unit testing. Tests can be run against multiple versions of the sample project, by modifying the project after it's created. This does not add significantly to test runtimes.

### 0.2.3

- Added documentation of [full set of CLI arguments](old_docs/cli_args.md).
- Progress towards supporting projects with a nested directory structure.
    - This is for projects started with `django-admin startproject project_name`, without a dot.
    - Includes nested version of sample blog project.
- Fixes bug on Windows, where system commands were not running.
- Steadily improving internal structure.

### 0.2.2

- Writes verbose log file; adds log directory to .gitignore.

### 0.2.1

- Simplified the integration testing scripts significantly.
- Added brief [roadmap](old_docs/roadmap.md).
- Added brief [contributing guide](old_docs/contributing.md).
- Added a [Code of Conduct](old_docs/code_of_conduct.md).
- SECRET_KEY on Heroku uses a config variable.
- DEBUG on Heroku uses a config variable.

### 0.2.0

- Preliminary support for Azure deployments.

0.1 - Supporting Heroku
---

### 0.1.11

- Supports Python 3.8, because Azure is still on 3.8.

### 0.1.10

- Bugfix to address import error in deploy_heroku.py.

### 0.1.9

- Bugfix: Minor bugs were causing issues with final message after deployment process had been completed.

### 0.1.8

- External changes:
    - `simple_deploy` accepts a `--platform` argument. The default, and only meaningful value at the moment is `heroku`. However, this change makes it possible to begin targeting other platforms.

- Internal changes:
    - Testing script is broken into platform-agnostic, and Heroku-specific files.
    - Test script accepts a platform argument: `$ autoconfigure_deploy_test.sh -o automate_all -p heroku`. Heroku is default value, and is the only meaningful value at the moment.

### 0.1.7

- Internal changes:
    - All multiline output messages defined in a separate module.
    - Reviewed all existing comments. (11/5/21)
    - Refactored code that adds Heroku-specific settings.

### 0.1.6

- Includes `--automate-all` flag.

### 0.1.5

- Supports projects that use Poetry.

### 0.1.4

- Supports projects that use Pipenv.

### 0.1.3

- Makes Heroku install from PyPI instead of the GitHub repo.

### 0.1.2

- Added change log.
- Expanded main README to include detailed steps, and more.

### 0.1.1

- Fixed markdown formatting issue on PyPI.

### 0.1.0

- Initial functionality; works for my project.