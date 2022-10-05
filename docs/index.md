# django-simple-deploy

`django-simple-deploy` configures your Django project for deployment to a number of different platforms. For some platforms, it can automate the entire deployment process. Currently, three platforms have preliminary support: [Fly.io](https://fly.io), [Platform.sh](https://platform.sh), and [Heroku](https://heroku.com).

Here's what automated deployment on [Fly.io](https://fly.io) looks like:

```
$ pip install django-simple-deploy
# Add simple_deploy to INSTALLED_APPS.
$ python manage.py simple_deploy --platform fly_io --automate-all
```

After these three steps, your project should open in a new browser tab. :)

Quick Start
---

For help deploying to a specific platform, start here:

- [Deploying to Fly.io](fly.io/quick_start.md)
- [Deploying to Platform.sh](platform.sh/quick_start.md)
- [Deploying to Heroku](heroku/quick_start.md)

More resources
---

- If you're not sure which platform to choose, here's an [overview](choosing_platform.md) of the different platforms.
- If you're interested in the motivations for `django-simple-deploy`, start with the [rationale](rationale.md).
- If you're interested in helping out, see the [contributing](contributing.md) page.