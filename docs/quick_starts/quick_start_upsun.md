---
title: "Quick Start: Deploying to Upsun"
hide:
    - footer
---

# Quick Start: Deploying to Upsun

## Overview

Deployment to Upsun can be fully automated, but the configuration-only approach is recommended. This allows you to review the changes that are made to your project before committing them and making the initial push. The fully automated approach configures your project, commits these changes, and pushes the project to Upsun's servers.

## Upsun Flex and Upsun Fixed

Upsun has two kinds of deployment plans, Flex and Fixed. Flex deployments allow you to make a wider range of choices when specifying resources, such as CPU and RAM. Once a Flex deployment has been made, you can adjust resource sizes as needed, or let Upsun adjust resource sizes for you. With Fixed deployments, you choose a plan with a fixed set of resources to start with. As your project grows, you have the option to upgrade to higher plan levels.

## Prerequisites

Deployment to Upsun requires three things:

- You must be using Git to track your project.
- You need to be tracking your dependencies with a `requirements.txt` file, or be using Poetry or Pipenv.
- The [Upsun CLI](https://docs.upsun.com/administration/cli.html) must be installed on your system, and you must have an Upsun account set up for their Fixed plan.

## Configuration-only deployment

First, install `django-simple-deploy`, and add `django_simple_deploy` to `INSTALLED_APPS` in *settings.py*:

```sh
$ pip install django-simple-deploy[upsun]
# Add "django_simple_deploy" to INSTALLED_APPS in settings.py.
$ git commit -am "Added django_simple_deploy to INSTALLED_APPS."
```

!!! note
    If you're using zsh, you need to put quotes around the package name when you install it: `$ pip install "django-simple-deploy[upsun]"`. Otherwise zsh interprets the square brackets as glob patterns.

Now create a new Upsun app using the CLI. You'll need to choose a name for your deployed project; a good choice is the same name as the one you used when running `django startproject`. Whatever name you choose, use that where you see `<project-name>`.

```sh
$ upsun create --title <project-name>
```

!!! note
    After creating a project, you'll find some auto-generated files in a new `.upsun/local/` directory. This is supposed to be ignored by Git, but that's currently [not working](https://github.com/platformsh/cli/issues/286) on Windows. You can add `.upsun/local/` to your .gitignore file on Windows for now, and this directory will be ignored. You'll need to commit this change before continuing, because django-simple-deploy looks for a clean Git status before making configuration changes in your project.

Now run the `deploy` command, using the same project name you used with the `upsun create` command:

```
$ python manage.py deploy --deployed-project-name <project-name>
```

At this point, you should review the changes that were made to your project. Running `git status` will show you which files were modified, and which new files were created.

If you want to continue with the deployment process, commit these changes and run the `push` command. When deployment is complete, use the `url` command to see the deployed version of your project:

```sh
$ git add .
$ git commit -m "Configured for deployment to Upsun."
$ upsun push
$ upsun url
```

You can find a record of the deployment process in `dsd_logs`. It contains most of the output you saw when running `deploy`.

## Automated deployment

If you want, you can automate this entire process. This involves just three steps:

```sh
$ pip install django-simple-deploy[upsun]
# Add `django_simple_deploy` to INSTALLED_APPS in settings.py.
$ python manage.py deploy --automate-all
```

You should see a bunch of output as Upsun resources are created for you, your project is configured for deployment, and `django-simple-deploy` pushes your project to Upsun's servers. When everything's complete, your project should open in a new browser tab.

## Pushing further changes

After the initial deployment, you're almost certainly going to make further changes to your project. When you've updated your project and it works locally, you can commit these changes and push your project again, without using `django-simple-deploy`:

```sh
$ git status
$ git add .
$ git commit -m "Updated project."
$ upsun push
```

Destroying projects
---

If you want to destroy a project on Upsun, be aware that there's a distinction between a *plan* and a *project*. If you destroy a plan, it usually destroys any projects associated with that plan. If you destroy a project, it may not destroy the associated plan.

Look at your [Upsun dashboard](https://console.upsun.com/), and make sure you're aware of any long-running projects that will accrue charges. You can destroy plans and projects by going to the Settings tab, and scrolling to the Delete button at the end of the page.

## Troubleshooting

If deployment doesn't work, please feel free to open an [issue](https://github.com/django-simple-deploy/django-simple-deploy/issues). Please share the OS you're  using locally, and the specific error message or unexpected behavior you saw. If the project you're deploying is hosted in a public repository, please share that as well.

