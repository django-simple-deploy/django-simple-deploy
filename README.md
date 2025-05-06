# django-simple-deploy

Deployment, for Djangonauts with deadlines.

## Documentation

The full documentation for this project is at [Read the Docs](https://django-simple-deploy.readthedocs.io/en/latest/).

## Quickstart

`django-simple-deploy` gives you a management command that configures your project for an initial deployment. It currently supports deployments to [Fly.io](https://fly.io), [Platform.sh](https://platform.sh), and [Heroku](https://heroku.com). Each platform is supported by an external plugin, which means it's relatively straightforward to build support for additional hosting platforms. A [plugin](https://github.com/django-simple-deploy/dsd-vps) supporting VPS-based deployments is currently in development.

If you have a Django project that runs locally, you can deploy your project in a few short steps. The only change you'll need to make to your project is to add `django_simple_deploy` to `INSTALLED_APPS`.

![Simplest example of how to use django-simple-deploy](https://raw.githubusercontent.com/ehmatthes/django-simple-deploy/main/assets/simplest_example.png)

The above command will deploy your project to Fly.io. To deploy to another platform such as Platform.sh, just install a different plugin when you install `django-simple-deploy`:

```sh
$ pip install "django-simple-deploy[platform_sh]"
```

All output is captured and written to a log file stored in `dsd_logs/`, which is placed at the project's root directory.

Installing a plugin automatically installs `django-simple-deploy`. So for platforms supported by third-party plugins, the only difference is the installation step:

```sh
$ pip install <dsd-plugin-name>
# Add django_simple_deploy to INSTALLED_APPS
$ python manage.py deploy --automate-all
```

Configuration-only mode
---

The above example uses the `--automate-all` flag, which reduces deployment to three steps. The fully automated mode configures your project, commits changes for you, and pushes your code to the target platform's servers. There's also a configuration-only mode, which lets you inspect the changes made to your project before committing them and making the actual deployment. For a quick example, see the full [Fly.io Quick Start guide](https://django-simple-deploy.readthedocs.io/en/latest/quick_starts/quick_start_flyio/).