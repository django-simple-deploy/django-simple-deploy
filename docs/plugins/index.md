---
title: Plugins
hide:
    - footer
---

# Plugins

Plugins are critical to the functioning of this project. Plugins don't just extend the functionality of django-simple-deploy; they implement *all* platform-specific functionality. The core project inspects the user's project and system, and then hands off to the plugin for all platform-specific configuration work.

## Developing a new plugin

If you want to write a plugin, see the notes in the [dsd-plugin-template](https://github.com/django-simple-deploy/dsd-plugin-template) repository. You can download (not clone) that repo, and you'll have a working plugin that you can adapt to the platform you're focusing on. If you're interested in developing a new plugin and want some help, please feel free to open an issue.


## Testing plugins

The test suite will identify a plugin that's installed in editable mode, and run that platform's unit and integration tests.

## More information

See the other pages in this section about [plugin utility functions](plugin_utils.md) and the `sd_config` [object](sd_config.md).