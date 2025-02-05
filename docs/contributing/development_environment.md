---
title: "Setting Up a Development Environment"
hide:
    - footer
---

# Setting Up a Development Environment

Setting up a development environment will let you make changes to `django-simple-deploy`, and deploy test projects using your version of `django-simple-deploy`. If your work improves the project, you can make a Pull Request and we'll review your changes to see if they're ready to be merged into the main project.

If you're doing any significant work, please open an issue and communicate with the rest of the team first. This project is evolving steadily, and we don't want to see people do a bunch of work that conflicts with other work that's being done, and can't end up being merged to the main project.

Also, if you haven't done so already, please review the [Testing on Your Own Account](own_account.md) page before moving forward.

## Make a local working copy of the project

First, fork the `django-simple-deploy` project on GitHub. If you haven't done this before, look for the Fork button in the upper right corner of the project's [home page](https://github.com/django-simple-deploy/django-simple-deploy/). This will copy the main branch of the project to a new repo under your account.

Next, clone your Github (replace `<username>` with your username):

```bash
$ git clone git@github.com:<username>/django-simple-deploy.git
# (You can use both SSH-based or HTTPS-based URLs.)
```

Add an `upstream` remote, then configure `git` to pull `main` from `upstream` and always push to `origin`:

```bash
$ cd django-simple-deploy
$ git remote add upstream https://github.com/django-simple-deploy/django-simple-deploy
$ git config branch.main.remote upstream
$ git remote set-url --push upstream git@github.com:<your-username>/django-simple-deploy.git
```

You can verify `git` is configured correctly by running:

```bash
$ git remote -v
origin  git@github.com:<username>/django-simple-deploy.git (fetch)
origin  git@github.com:<username>/django-simple-deploy.git (push)
upstream        https://github.com/django-simple-deploy/django-simple-deploy (fetch)
upstream        git@github.com:<username>/django-simple-deploy.git (push)

$ git config branch.main.remote
upstream
```

If you did everything correctly, you should now have a copy of the code in the `django-simple-deploy` directory and two remotes that refer to your own GitHub fork (`origin`) and the official **django-simple-deploy** repository (`upstream`).

Now, considering that you are in the *django-simple-deploy/* directory, create a virtual environment and install the necessary dependencies:

=== "macOS/Linux"

    ```
    $ python -m venv .venv
    $ source .venv/bin/activate
    $ pip install --upgrade pip
    $ pip install -e '.[dev]'
    ```

=== "Windows"

    ```
    > python -m venv .venv
    > .venv\Scripts\activate
    > pip install --upgrade pip
    > pip install -e '.[dev]'
    ```


## Make a test project to run `django-simple-deploy` against

In order to work on `django-simple-deploy`, you need a Django project outside the main project directory to run the `deploy` command against. You can either copy a project from the `sample_project/` directory, or clone the [standalone sample project](https://github.com/ehmatthes/dsd_sample_blog_reqtxt).

### Copy a project from `sample_project/`

The projects in `sample_project` contain multiple dependency management files. No real-world Django project would have this combination of files; it's set up this way to support automated testing of multiple dependency management systems. During testing, the unneeded files are removed so that the target dependency management system can be tested.

If you're going to copy a project from this directory, start by copying the entire project, such as `blog_project/`, to a directory outside the `django-simple-deploy/` directory. Then choose a dependency management system: bare `requirements.txt` file, Poetry, or Pipenv. Remove the files not needed for the dependency management system.

=== "Bare requirements.txt file"

    Remove `Pipfile` and `pyproject.toml`.

=== "Poetry"

    Remove `requirements.txt` and `Pipfile`.

=== "Pipenv"

    Remove `requirements.txt` and `pyproject.toml`.

### Copy the standalone test project

The [standalone test project](https://github.com/ehmatthes/dsd_sample_blog_reqtxt) is maintained to make it easier for people to [document a test run](test_run.md). You are welcome to use this project when working on `django-simple-deploy`.

Clone the test repo to a directory outside of the `django-simple-deploy/` directory:

```sh
$ git clone https://github.com/ehmatthes/dsd_sample_blog_reqtxt.git
```

## Make sure the test project works

The core idea of `django-simple-deploy` is that if you have a simple but nontrivial Django project that works locally, we can help you deploy it to a supported platform. Let's make sure the project works locally before trying to deploy it. The following instructions work with a `requirements.txt` file; you'll follow a similar process for other dependency management systems such as Poetry or Pipenv.

In the root directory of the test project, build out the environment and start the development server:

=== "macOS/Linux"

    ```
    $ python -m venv b_env
    $ source b_env/bin/activate
    $ pip install --upgrade pip
    $ pip install -r requiremnents.txt
    $ python manage.py migrate
    $ python manage.py runserver
    ```

=== "Windows"

    ```
    > python -m venv b_env
    > b_env\Scripts\activate
    > pip install --upgrade pip
    > pip install -r requiremnents.txt
    > python manage.py migrate
    > python manage.py runserver
    ```

Open a new terminal tab and run the functionality tests against the local project:

=== "macOS/Linux"

    ```
    $ source b_env/bin/activate
    $ python test_deployed_app_functionality.py --url http://localhost:8000
    ```

    The tests expect an empty database to start. If you've already entered sample data, run the tests with the `--flush-db` flag:

    ```
    $ python test_deployed_app_functionality.py --flush-db --url http://localhost:8000
    ```

=== "Windows"

    ```
    > b_env\Scripts\activate
    > python test_deployed_app_functionality.py --url http://localhost:8000
    ```

    The tests expect an empty database to start. If you've already entered sample data, run the tests with the `--flush-db` flag:

    ```
    > python test_deployed_app_functionality.py --flush-db --url http://localhost:8000
    ```

If the tests pass, you're ready to run a deployment using your local version of `django-simple-deploy`.

## Make a new commit

Before you run the `deploy` command, make a commit so you can more easily do repeated deployments without having to build the test project from scratch:

```sh
$ git add .
$ git commit -am "Initial state, before using django-simple-deploy."
```

## Make an editable install of `django-simple-deploy`

To use your local version of `django-simple-deploy`, we'll install `django-simple-deploy` using an [editable install](https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs). Normally `pip install` copies a package's files to your environment. Changes to the source files aren't copied to your environment until you upgrade or reinstall the package. With an editable install, pip instead sets up the project so the package is imported into the environment each time it's used. This means you can make changes in your `django-simple-deploy/` directory, and those changes will be used in your test project the next time you run the `deploy` command.

Here's how to make the editable install:

```sh
$ pip install -e /local/path/to/django-simple-deploy/
```

## Install the correct plugin for your platform

There are currently three plugins available: [dsd-flyio](https://github.com/django-simple-deploy/dsd-flyio), [dsd-platformsh](https://github.com/django-simple-deploy/dsd-platformsh), and [dsd-heroku](https://github.com/django-simple-deploy/dsd-heroku). Pick the one that you want to use for deployment, and install it just like any PyPI package:

```sh
$ pip install dsd-flyio
```

!!! note
    If you want to contribute to a plugin as well, clone the plugin to your system just like you did for django-simple-deploy, and make an editable install of the plugin into your test project as well.

## Run `django-simple-deploy` against the test project

Now, visit the [Quick Start](../quick_starts/index.md) page for the platform you want to target, and follow the directions you see there. Make sure you skip the `pip install django-simple-deploy` step, because we've already made the editable install of this package.

### Test the deployment

To make sure the deployment worked, run the functionality tests against the deployed version of the sample project:

```sh
$ python test_deployed_app_functionality.py --url https://deployed-project-url
```

Keep in mind that the `--flush-db` command will not work on a deployed project. Also, note that these automated tests don't always work on projects that are deployed using the lowest-tier resources on the target platform. If you see the deployed site in the browser but the tests fail, try clicking through different pages and making a user account. It's possible that the project works for manual use, but doesn't respond well to rapid automated test requests.

### Destroy the remote resources

At this point, you can destroy the remote resources that were created. Remote resources should be destroyed automatically when running integration tests, but they are not destroyed for you when testing in the manner we've just run through. If you have any questions about this, see the [Testing on Your Own Account](own_account.md) page.

### Reset the test project

After verifying that your local version of `django-simple-deploy` works when run against the test project, you'll need to reset the test project. This will let you modify `django-simple-deploy`, and then run the `deploy` command again and see the effect of your changes.

To reset the project, run `git reset --hard commit_hash`, using the hash of the commit that you made after making sure the test project works locally. Also, run `git status` and make sure you remove any files or directories that are left in the project, such as `dsd_logs/`. The `.platform/` directory also tends to hang around after resetting the test project, when testing against Platform.sh. The command `git clean -fd` will remove any new files and directories that were created during configuration.

## Developing `django-simple-deploy`

Now you're ready to do your own development work on `django-simple-deploy`. Make a new branch on your fork of the project, and make any changes you want to the codebase. When you want to see if your changes improve the configuration and deployment process, go back to the [Run `django-simple-deploy` locally](#run-simple_deploy-against-the-test-project) section and repeat those steps.

### Helpful flags for development work

The `--unit-testing` and `--ignore-unclean-git` flags can be really helpful when doing development work. For example say you're revising the approach to generating a dockerfile for Poetry users when deploying to Fly.io. You've modified some of the project's code, and you want to see how it impacts your demo project. Run the following command:

```sh
$ python manage.py deploy --unit-testing
```

This won't run the unit tests, but it will skip the same network calls that are skipped during unit testing. You should see most of the same configuration that's done during a normal run, using sample resource names.

When you've made more changes and want to run the `deploy` command again, but all you're interested in is the Dockerfile that's generated, run the following two commands:

```sh
$ rm Dockerfile
$ python manage.py deploy --unit-testing --ignore-unclean-git
```

This will avoid network calls and use sample resource names again, and it will ignore the fact that you have significant uncommitted changes. A new Dockerfile should be generated, and you can repeat these steps to rapidly develop the code that generates the Dockerfile.

## Running tests

Unit and integration tests can be run locally, without making any network calls. End-to-end tests are one-off runs of actual deployments, and can cost money to run. If you're interested in running tests, see the [Testing](../../testing/) section.

## Making a PR

Unit and integration tests should pass before making a PR. If you're having trouble getting those tests to pass, please ask for help by opening an issue.

You *should* run the end-to-end tests for at least one platform before submitting a PR. If you're just working on core django-simple-deploy, I'd suggest using the `dsd-flyio` plugin for testing. If you're developing a different plugin, use that plugin's tests.

If you can't run an end-to-end test, please ask for help in an issue.

## Ongoing work

It's a lot of work to do these steps repeatedly. You can automate most of this setup work with the following commands. For the moment, this assumes you have a directory called *projects/* in your home directory:

```sh
$ python tests/e2e_tests/utils/build_dev_env.py
--- Finished setup ---
  Your project is ready to use at: /Users/eric/projects/dsd-dev-project_zepbz
```

Now, in a separate terminal tab or window:

```sh
$ cd /Users/eric/projects/dsd-dev-project_zepbz
$ source .venv/bin/activate
(.venv)$ python manage.py migrate
(.venv)$ git log --pretty=oneline
a0ebc9 (HEAD -> main) Added django_simple_deploy to INSTALLED_APPS.
7209f0 (tag: INITIAL_STATE) Initial commit.
```

This gives you a project where `django-simple-deploy` has already been installed and added to `INSTALLED_APPS`. Basically, you should be able to just run the `deploy` command at this point. If you want to run `deploy` more than once, you can git reset back to `INITIAL_STATE`.

New contributors should probably go through the longer process once, unless they've used `django-simple-deploy` previously.

You can also pass arguments to *build_dev_env.py* to develop against the package manager of your choice, and you can run manual tests against the PyPI version if you wish as well:

```sh
$ python build_dev_env.py --pkg-manager [req_txt | poetry | pipenv] --target [development_version | pypi]
```

## Closing thoughts

This is an evolving project. Please feel free to open an [issue](https://github.com/django-simple-deploy/django-simple-deploy/issues/new/choose) or a [discussion](https://github.com/django-simple-deploy/django-simple-deploy/discussions/new) about any aspect of this project.
