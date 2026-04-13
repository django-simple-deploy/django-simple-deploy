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
