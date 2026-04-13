---
title: User Stories
hide:
    - footer
---

# User stories

What are the use cases for django-simple-deploy, from a user's perspective? Having a few specific examples is helpful for discussions about which plugins to prioritize, and which options to make available to users.

## 1: New to Django, new to deployment

Someone just finished the official [Polls tutorial](https://docs.djangoproject.com/en/6.0/intro/tutorial01/), the [Django Girls tutorial](https://tutorial.djangogirls.org/en/), or another introductory Django tutorial. They want to see their project running on a live server, and maybe share it with friends, or keep it live for a presentation.

Typical of this user:

- Wants a free deployment option, ideally without the requirement of having a credit card on file with the host.
- Will probably not keep the deployment live for very long. Maybe 30-60 minutes to run it and try it out, maybe a week or two for a presentation.
- May want to deploy, destroy, and redeploy several times for practice.
- May also be new to Git, SSH, dependency management, and other secondary but quite necessary skills/ knowledge.

## 2: Small personal project, long-term deployment

The user has created a personal project that works locally, and they want to deploy it and keep building. They may use some external services such as an email authentication system, but they are not planning to monetize the project.

Typical of this user:

- They're willing to pay a reasonable cost. They may want to minimize the cost, or they may be willing to spend a little more for a more robust and resilient deployment.
- They may have needs like background tasks.
- They will run `deploy` once, and then should never need django-simple-deploy for this project again.
- More likely to be familiar with Git and dependency management than #1, but still may be new to things like SSH keys.

## 3: Small to medium project, with potential monetization/ business use

The user has built a project that may be monetized, such as a small SAAS project. They want a long-term, reliable deployment, and they'll likely have more parts involved, such as email authentication, background tasks, and e-commerce integrations.

- They're more likely to pay a reasonable cost, although they want to maximize efficiency for their deployment. They don't want to over-provision at this point.
- They may not want to start out on the lowest level resources, ie the cheapest instance on a platform.

## 4: Experienced developers, exploring a new platform or deployment approach

This user has deployed Django projects previously, and can do a deployment on their own if needed. But they can learn a new platform faster by running `manage.py deploy`, followed by `git diff`. They may be focusing on a platform that's new to them, or a different approach on a familiar platform.

- This user is probably not interested in a long-term deployment. Their deployment can be similar to #1, but their interest and motivation is quite different.
