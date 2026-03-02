---
title: "Contributing Quick Start"
hide:
    - footer
---

This is meant to be a streamlined version of the rest of what you'll find in the Contributing docs.

## Make a local development copy of django-simple-deploy

Plugins and the core django-simple-deploy all need to be in the same parent directory for development work. For this guide, I'll call that directory `dsd_work/`.

First, fork the `django-simple-deploy` project on GitHub. Then clone your fork of the project to your local system. (You can copy the git URL from your fork.) Build a development environment, and run local tests:

```bash
$ mkdir dsd_work && cd dsd_work
dsd_work$ git clone git@github.com:<username>/django-simple-deploy.git
dsd_work$ cd django-simple-deploy
django-simple-deploy$ uv venv .venv
django-simple-deploy$ source .venv/bin/activate
django-simple-deploy$ uv pip install -e '.[dev]'
django-simple-deploy$ pytest
```

All tests should pass.

## Make a local development copy of dsd-flyio

Even if you're not going to work on the Fly.io plugin, it's the plugin that's used for django-simple-deploy core's integration tests. You don't need to have a Fly.io account.

Make sure you're starting from the parent directory, in this example `dsd_work/`. If you want to contribute to dsd-flyio, fork it and clone your own copy of the repo. Otherwise, you can clone from the offical repo.

```bash
dsd_work$ git clone https://github.com/django-simple-deploy/dsd-flyio.git
dsd_work$ cd dsd-flyio
dsd-flyio$ uv venv .venv
dsd-flyio$ source .venv/bin/activate
dsd-flyio$ uv pip install -e '.[dev]'
```

## Run django-simple-deploy's full set of integration tests

The core project can only run its full set of integration tests when a plugin is installed. Note that these steps take place in the `django-simple-deploy/` local repo:

```bash
django-simple-deploy$ uv pip install -e ../dsd-flyio
django-simple-deploy$ uv pip freeze | grep dsd-
-e file:///Users/eric/dsd_work/dsd-flyio
django-simple-deploy$ pytest
```

All tests should pass, and you should see many more tests than what you saw before installing the plugin.

## Build a disposable sample project for development work

django-simple-deploy, and the plugins, only work in the context of a Django project. There's a tool to create a sample project alongside django-simple-deploy and any plugins you're working on. This example uses the Fly.io plugin, but again you don't need a Fly account to see how this works:

Start from the `django-simple-deploy/` directory:

```bash
django-simple-deploy$ python tests/e2e_tests/utils/build_dev_env.py
...
 --- Finished setup ---
  Your project is ready to use at: /Users/eric/dsd_work/dsd-dev-project_biop0
```

Now you have a sample project, with an editable installation of django-simple-deploy to work with. In this project, `django_simple_deploy` has already been added to `INSTALLED_APPS`, and it has a Git history that's useful for development work.

You can navigate to this project, activate the virtual environment, and poke around the project.

```bash
dsd_work$ cd dsd-dev-project_biop0
dsd-dev-project_biop0$ source .venv/bin/activate
dsd-dev-project_biop0$ git log --pretty=oneline
fcd045 (HEAD -> main, tag: ADDED_DSD) Added django_simple_deploy to INSTALLED_APPS.
b43af3 (tag: INITIAL_STATE) Initial commit.
```

Run the project locally, and satisfy yourself that it's working.

```bash
dsd-dev-project_biop0$ python manage.py runserver
```

Now you can make an editable install of a plugin, and run it in a local-only testing mode:

```bash
dsd-dev-project_biop0$ uv pip install -e ../dsd-flyio
dsd-dev-project_biop0$ python manage.py deploy --unit-testing
```

The flag `--unit-testing` here would probably be better changed to `--local-testing`. You can now run `git status`, `git log`, `git diff`, and see what changes were made to the project. 

If you were developing a plugin, you'd want to make changes to the plugin and then run `deploy` again. That's easy to do in this dev project environment:

```bash
dsd-dev-project_biop0$ git reset --hard INITIAL_STATE && git clean -fd
dsd-dev-project_biop0$ python manage.py deploy --unit-testing
```

Whenever you're ready, you can leave off the `--unit-testing` flag, and see if your plugin makes an actual deployment.

You can use the same dev project for a lot of development work. Just be aware that some plugins add a variety of git remotes, or other subtle change. These are throwaway projects. Any time you want, you're free to destroy the `dsd-dev-project_<project-id>/` directory, and make a fresh one for your next phase of work.