---
title: Roadmap
hide:
    - footer
---

# Roadmap

The 1.0 release indicates reliable performance for all officially-supported plugins, and a stable platform on which to expand the plugin ecosystem.

Ongoing development is focused on improving the internal codebase, and making it easier to build and maintain plugins. The items below are not in order of priority, but describe the different directions this project is heading.

---

## Promotion and feedback

As the plugin ecosystem expands, this project becomes useful to more Django developers. It's important to continue making people aware of the project, and that it's in a stable and usable state. As usage expands, consider the feedback that comes in as bug reports come in, and boundaries of the project are identified.

It would also be good to showcase specific use cases, and demonstrate how django-simple-deploy can be used with a number of specific projects. These projects include the polls project from the official tutorial and the Django Girls project. It would also be nice to refine the sample project used for testing, into a project that could be used by anyone working on Django itself.

## Expand contributor base

I've done multiple sprints at various Python and Django conferences over the past few years. This project has always drawn about 5 to 12 contributors during sprints. But it was hard for people to keep contributing with the project in a state of rapid change. Now that it's more stable, it would be good to encourage contributors, with a focus on finding people who have expertise with specific platforms and approaches to deployment.

## Improve approach to managing user's project requirements

django-simple-deploy first examines the user's project and system. It identifies the project requirements, and usually adds a small set of deployment-specific requirements. We need to do this in a way that's compatible with the user's requirements specification file, and the way they manage requirements in their project.

Packaging and dependency management have been rapidly evolving as django-simple-deploy underwent pre-1.0 development. One of the most important ongoing tasks is to continue refining the current approach, and adapt to newer approaches.

## Support nested and non-nested Django projects

When you run `startproject` you can choose whether to run it with or without a trailing dot. The trailing dot, ie `django-admin startproject blog .` tells Django to place `manage.py` in the root directory of the project. This is a "non-nested project", because `manage.py` is not nested within the project. if you leave out the dot, `manage.py` is placed in an inner directory, creating a nested project structure.

This affects deployment on platforms that expect to find `manage.py` in the root project folder.

## Friendly summary of deployment process

All runs of `simple_deploy` produce a log file, which is helpful for troubleshooting. But it would be really nice to produce a friendly summary of the deployment process that briefly describes what was done, how to redeploy the project after making more changes locally, and how to start understanding the target platform's documentation.

This would clearly help beginners, but it's one of those things that's just as useful for experienced people. It's like a cheatsheet for a platform, with the advantage of being customized to the user's project and deployment. It's not meant to replace the platform's documentation. Rather, it's meant to offer an efficient onboarding into the platform's docs, which plugin developer have probably already become familiar with. We've done the work to find the most important parts of a platform's documentation; we might as well let our users learn from what we've learned.


!!! note
    A very preliminary level of support was built for Heroku, as a proof-of-concept. This shouldn't be a difficult task, and it should be really satisfying to implement. The POC work is on the [friendly_summary](https://github.com/django-simple-deploy/django-simple-deploy/tree/friendly_summary) branch. That branch is way out of date (it pre-dates the plugin model), but there might be something helpful in there.

## Refine core plugins

The three official plugins should serve as exemplars. They should be well-structured, well-commented, and demonstrate how people might create plugins for other platforms. Capture any feedback from people who know these platforms better than I do, so we end up with an exemplary deployment process on each platform.

## Expand plugin system to demonstrate specific capabilities

As the maintainer of the core django-simple-deploy tool and the overall ecosystem, I should not be writing a bunch of new plugins. That misses the point of fostering a collaborative ecosystem where people are working on the parts they know best.

That said, it would be really helpful to write a small set of plugins that demonstrate new areas where this project is applicable. The clearest example is writing a plugin that supports deployment to a general VPS provider. That approach could then be replicated by others for a number of other VPS providers.

This may lead to a smoother onboarding approach to building new plugins. There's probably a way to have an abstract VPS plugin, which can then be used for a variety of VPS providers with just the provider-specific customization.

## Refine features that support plugin development

There are a number of utilities in django-simple-deploy that are useful to plugin developers. For example the `dsd_config` object provides information about the user's system and project that was discovered during initial inspection. Also, the `plugin_utils` module offers a number of utility functions for common actions that need to be taken during configuration work.

These tools can be refined, and I'm sure there are some utilities that could be added. The goal is not so much to continue expanding the core django-simple-deploy tool, but to reduce the amount of redundant work we see across the plugin ecosystem.

## Start contributing

If you're interested in any of this, please feel free to open an [issue](https://github.com/django-simple-deploy/django-simple-deploy/issues) or start a [discussion](https://github.com/django-simple-deploy/django-simple-deploy/discussions). If you want to start writing your own plugin, see the [Plugins](../plugins) section here, and also see the [dsd-plugin-template](https://github.com/django-simple-deploy/dsd-plugin-template) repository.