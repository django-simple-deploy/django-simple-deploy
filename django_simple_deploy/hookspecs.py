"""Hook specs for django-simple-deploy.

The name `simple_deploy_deploy()` is a bit awkward, but it follows the convention of
naming plugins in pluggy:
  <plugin_name>_<function_name>()
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
def dsd_deploy():
    """Carry out all platform-specific configuration and deployment work."""
