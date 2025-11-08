---
title: "The dsd_pre_inspect() hook"
hide:
    - footer
---

# The `dsd_pre_inspect()` hook

In the overall workflow, django-simple-deploy inspects the user's project and system *before* handing off to the plugin for platform-specific configuration work. This is for two reasons:

- We want to find all the information that plugins are likely to need, and define common utility functions that all plugins can use.
- If there's any reason to think configuration won't work, we want to bail as early as possible, *before* making any changes to the user's project.

That has worked well, and you should avoid doing any work before the final handoff from core to the plugin. That is, all of your work should happen in the *platform_deployer.py* file.

There are some exceptions where a bit of work needs to be done before core has a chance to inspect the user's project. For example, one platform's CLI generates some local-only files after running their `create` command. Those files are supposed to be ignored, by an entry in `.git/info/exclude`. That platform's CLI does not write the ignore rule correctly in the `exclude` file. This is the kind of small issue that some platforms never fix. In this case, it prevents the user from having a clean git status before running `manage.py deploy`.

The `dsd_pre_inspect()` hook exists for this kind of situation. This hook is called before inspecting the user's project. Use it sparingly. If you do use it, you can return a message about what was done during the pre-inspection phase. This message will be handled just as all other messages are handled.
