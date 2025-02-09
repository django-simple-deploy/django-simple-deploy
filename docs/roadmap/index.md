---
title: Roadmap
hide:
    - footer
---

# Roadmap

The 1.0 release indicates reliable performance for all officially-supported plugins, and a stable platform on which to expand the plugin ecosystem.

Ongoing development is focused on improving the internal codebase, and making it easier to build and maintain plugins.

## Support nested and non-nested Django projects

When you run `startproject` you can choose whether to run it with or without a trailing dot. The trailing dot, ie `django-admin startproject blog .` tells Django to place `manage.py` in the root directory of the project. This is a "non-nested project", because `manage.py` is not nested within the project. if you leave out the dot, `manage.py` is placed in an inner directory, creating a nested project structure.

This affects deployment on platforms that expect to find `manage.py` in the root project folder.

## Friendly summary of deployment process

All runs of `simple_deploy` produce a log file, which is helpful for troubleshooting. But it would be really nice to produce a friendly summary of the deployment process that briefly describes what was done, how to redeploy the project after making more changes locally, and how to start understanding the target platform's documentation.

This would clearly help beginners, but it's one of those things that's just as useful for experienced people. It's like a cheatsheet for a platform, with the advantage of being customized to the user's project and deployment. It's not meant to replace the platform's documentation. Rather, it's meant to offer an efficient onboarding into the platform's docs, which plugin developer have probably already become familiar with. We've done the work to find the most important parts of a platform's documentation; we might as well let our users learn from what we've learned.


!!! note
    A very preliminary level of support was built for Heroku, as a proof-of-concept. This shouldn't be a difficult task, and it should be really satisfying to implement. The POC work is on the [friendly_summary](https://github.com/django-simple-deploy/django-simple-deploy/tree/friendly_summary) branch. That branch is way out of date (it pre-dates the plugin model), but there might be something helpful in there.
