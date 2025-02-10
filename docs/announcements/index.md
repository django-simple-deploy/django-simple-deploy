---
title: Announcements
hide:
    - footer
---

# Announcements

---

*2/10/2025*

## `django-simple-deploy` 1.0.0 is out

It's been a long time coming, so I'm happy to announce that django-simple-deploy 1.0 has just been released. 1.0.0 is just a number, so what does it mean for this project in particular? It really boils down to two things: reliability, and stability.

### Reliability

From this point forward, deploying a relatively simple Django project to platforms supported by official plugins should work on all three operating systems. Currently, the official plugins support deployment to [Fly.io](https://fly.io), [Platform.sh](https://platform.sh), and [Heroku](https://www.heroku.com). If you use django-simple-deploy for deployment to any of these platforms and it doesn't work, please open an [issue](https://github.com/django-simple-deploy/django-simple-deploy/issues).

### Stability

django-simple-deploy should be stable from this point forward in two main ways. The user-facing API should remain stable for the foreseeable future. That means teachers, authors, and other content creators should be able to use django-simple-deploy in Django-focused resources, without having to update their resources on a regular basis. When a platform's deployment process changes, plugins may have to be updated, but end users won't notice any difference. They'll still install django-simple-deploy and a plugin, add `django_simple_deploy` to `INSTALLED_APPS`, and then run the `deploy` command.

Also, the core-plugin interface should be stable from this point forward. That means plugin developers should be able to build out support for new platforms, and a variety of approaches for some platforms, without worrying about breaking changes coming from this project. Any changes that do affect the core-plugin interface will be handled in a way that prioritizes clear communication with plugin developers, and backwards compatibility.

### Looking forward

If you're interested in knowing more details about what lies ahead for this project, see the [Roadmap](../roadmap). The roadmap has just been updated to focus on post-1.0 plans.


### Historical note

django-simple-deploy started as an attempt to automate the boilerplate configuration work everyone had to do each time they pushed a Django project to Heroku. Getting that to work was satisfying, but it felt like I was doing Heroku's work for them. That led to the idea of building a deployment tool that was primarily focused on supporting Django developers in general, not just one specific hosting platform.

### Thank you

I've been working on this project off and on for years at this point. Lots of people have contributed code, wishes, technical thoughts, and general support. If you're one of those people, thank you so much - you've absolutely contributed to the overall vision for a simpler deployment story for every Django developer.

- Eric