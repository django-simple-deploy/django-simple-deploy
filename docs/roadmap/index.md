---
title: Roadmap
hide:
    - footer
---

# Roadmap

The 1.0 release indicates reliable performance for all officially-supported plugins, and a stable platform on which to expand the plugin ecosystem.

Ongoing development is focused on improving the internal codebase, and making it easier to build and maintain plugins.


## Friendly summary of deployment process

All runs of `simple_deploy` produce a log file, which is helpful for troubleshooting. But we also aim to produce a friendly summary of the deployment process that briefly describes what was done, how to redeploy the project after making more changes locally, and how to start understanding the target platform's documentation.

| Fly.io | Platform.sh | Heroku |
| :--------------------------: | :----: | :----: |
| :fontawesome-regular-square: | :fontawesome-regular-square: | :fontawesome-regular-square-check: |

!!! note
    A very preliminary level of support was built for Heroku, as a proof-of-concept. This is not a difficult task, and it will be enjoyable to fill out this table.

    `simple_deploy` aims to make the initial deployment process friendlier and less error-prone, but our goal is also to help people become comfortable with their chosen platform. This friendly summary just provides some helpful jumping-off points, so people don't have to approach their platform's documentation completely on their own. We're basically pointing users to the parts of a platform's documentation that have been most relevant and helpful in understanding Python deployments on that platform.

## Support nested and non-nested Django projects

When you run `startproject` you can choose whether to run it with or without a trailing dot. The trailing dot, ie `django-admin startproject blog .` tells Django to place `manage.py` in the root directory of the project. This is a "non-nested project", because `manage.py` is not nested within the project. if you leave out the dot, `manage.py` is placed in an inner directory, creating a nested project structure.

This matters to platforms because some platforms look for `manage.py` in the root project folder.

| Project Structure | Fly.io | Platform.sh | Heroku |
| :------: | :--------------------------: | :----: | :----: |
| non-nested projects | :fontawesome-solid-square-check: | :fontawesome-solid-square-check: | :fontawesome-solid-square-check: |
| nested projects | :fontawesome-regular-square: | :fontawesome-regular-square: | :fontawesome-regular-square: |

!!! note
    Some work has been done to attempt support on Heroku, but that's probably the most difficult platform to support. This table will fill in more quickly when there's time to look at projects that use a Dockerfile, where we can move files around during every deployment push without affecting the local project.
