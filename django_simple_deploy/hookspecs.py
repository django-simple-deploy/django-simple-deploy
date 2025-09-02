"""Hook specs for django-simple-deploy."""

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
def dsd_get_plugin_cli_args(parser):
    """Get plugin-specific CLI args."""

@hookspec
def dsd_deploy():
    """Carry out all platform-specific configuration and deployment work."""
