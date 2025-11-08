"""Hook specs for django-simple-deploy.

The order here should match the order in which hooks are called by core.
"""

import pluggy

hookspec = pluggy.HookspecMarker("django_simple_deploy")


@hookspec
def dsd_get_plugin_config():
    """Get plugin-specific attributes required by core.

    Required:
    - automate_all_supported
    - platform_name
    Optional:
    - confirm_automate_all_msg (required if automate_all_supported is True)
    """

@hookspec
def dsd_get_plugin_cli(parser):
    """Get plugin's CLI extension."""

@hookspec
def dsd_validate_cli(options):
    """Validate the plugin-specific CLI args."""

@hookspec
def dsd_pre_inspect():
    """Allow plugin to do work before core inspects the user's project.

    You should only use this hook if there's something that *must* happen
    before core inspects the user's project. We want to do all the core work
    before the plugin modifies the project. We want the chance to find any
    reasons we'll have to bail before making configuration changes.

    The motivation for this hook is that a plugin needed to address a bug in how
    a platform's CLI mishandled Git exclude files. If the plugin can't do
    pre-inspection work, that plugin will never pass the git status check that
    core runs before handing off to the plugin. This hook allows that plugin
    to address a bug that the upstream CLI hasn't yet addressed. This is
    exactly the kind of buffer we want to be, between the user and the platform.

    Please use this hook sparingly, if at all.

    See: https://github.com/django-simple-deploy/django-simple-deploy/issues/466
    """

@hookspec
def dsd_deploy():
    """Carry out all platform-specific configuration and deployment work."""
