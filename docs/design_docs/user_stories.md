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

## 2: Side project developer

Someone with a few years of Django experience who builds side projects in their spare time. They've deployed projects before, but the process has always involved a lot of manual steps — reading platform docs, setting environment variables, configuring databases, debugging `staticfiles`. They'd like to launch new side projects quickly without spending a whole weekend on deployment configuration.

Typical of this user:

- Has an existing Django project that works locally and wants it live within an hour.
- Comfortable with the command line, but doesn't want to learn platform-specific CLIs in depth.
- Values repeatability: if they start a second side project next month, they want the same smooth deployment experience.
- Is okay with a paid tier if it's affordable (e.g. $5–$10/month), but wants to understand costs upfront.
- May want to tear down and redeploy to a different platform if pricing or features change.

## 3: Bootcamp graduate showcasing portfolio work

Someone who recently completed a web development bootcamp and has built a Django project they want to show to potential employers. The project needs to stay live reliably during a job search, which could last weeks or months. Deployment docs they've found so far assume more DevOps knowledge than they have.

Typical of this user:

- Needs a stable, always-on deployment (not a free tier that sleeps after inactivity).
- Wants a shareable URL they can put on a resume or LinkedIn profile.
- Has limited time to debug deployment issues — needs the process to "just work."
- May have never configured a production database, `ALLOWED_HOSTS`, or `SECRET_KEY` for deployment before.
- Will likely stick with whatever platform they deploy to first, so first-time success matters a lot.

## 4: Experienced developer migrating away from Heroku

A professional Django developer whose team has been on Heroku for years. Following Heroku's removal of the free tier (and rising costs), they need to migrate one or more apps to a different platform. They want a migration path that doesn't require rewriting infrastructure-as-code from scratch.

Typical of this user:

- Has several existing Django projects already in production, some with background workers, scheduled tasks, or multiple services.
- Wants to validate that the new platform works before fully committing, so a side-by-side trial deployment is appealing.
- Comfortable with Python, pip, and git; less interested in learning Docker or Kubernetes just for a small app.
- Cares about minimizing downtime during migration.
- May need to convince a manager or team that the new platform choice is sound — a well-documented, repeatable process helps.
