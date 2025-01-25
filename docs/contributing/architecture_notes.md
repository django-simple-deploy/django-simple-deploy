---
title: Architecture Notes
hide:
    - footer
---

# Architecture Notes

This page describes some aspects of the structure of the project.

## Platform-specific messages

The `deploy.py` script needs access to some platform-specific messages. The plugin should provide those messages.

## Checking for unit testing

There are many network calls that don't need to be made when unit testing. These checks are typically placed at the lowest level possible, to keep the workflows in higher level methods simple and readable.

## Checking for `--automate-all`

Likewise, checks for automate-all are usually in lower-level functions, to keep higher-level functions simpler.

---

## Contract between host and plugin

This is a parking lot for notes about implementing the plugin model.

### What does the host provide the plugin?

- Host inspects project, and makes relevant information about the project available, such as path to root directory, OS, package manager in use, etc. For a full list of what's shared with the plugin, see `utils/dsd_config.py`.
- Utility functions for common operations, such as writing to the log file and writing to the console, and running fast and slow subprocess commands.

### What must the plugin provide to the host?

- A hook function named `dsd_get_plugin_config()`. This provides the core project with some information about how the plugin handles deployment, which is used during some of the inspection and setup work.
- A hook function named `dsd_deploy()`. Once the project has been inspected and setup work has been completed, the plugin takes care of the rest of the platform-specific configuration and deployment work.
- See `hookspecs.py` for more specific requirements.

    
### What *should* the plugin do?

These are not hard requirements, but should probably be done by every deploy script. This may separate out into CLI-based workflows, API-based workflows, and GH-based workflows.

- Verify that the platform's CLI is installed.
- Verify that the user has authenticated through the CLI.
- Verify that any pre-requisite resources have already been created.

See the [plugins](../../plugins/) section for more information.