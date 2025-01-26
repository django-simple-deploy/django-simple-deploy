---
title: Strengths and Limitations
hide:
    - footer
---

# Strengths and Limitations

## Strengths

### You can choose a hosting platform *after* you have a working project

Many platforms' deployment docs tell you how to modify your project's settings so it will work on their infrastructure. This often involves conditional settings and environment variables. It's not uncommon for platforms to show you the settings that work on their platform, and leave it to you to sort out how to make sure these settings take effect on their platform, without affecting your local working environment.

It's also common for a platform's docs to point to a working demo of a Django project. The platform-specific settings are often interspersed with Django's default settings, and again it's up to you to find those settings and figure out how to incorporate them into your project, and do so in a way that doesn't interfere with your local development environment.

Lastly, some platforms and other packages offer a template you can start with so your project will end up working on a particular platform. This requires you to choose a target deployment platform *before* you begin working on your project. This isn't the way many people get to their first deployment. Rather, they build a project and like how it works locally, and then realize they'd like to make their project available to others.

### It sets up a feedback cycle between platform providers and Django experts

At one point I was writing the deployment script for a newly-supported platform. The deployment process for this platform involves creating a Dockerfile, so I adopted the sample Dockerfile the host provides in their onboarding documentation. Someone much more experienced with deployment commented that there's a way to significantly reduce the size of the resultant Docker image. The final version of the `django-simple-deploy` configuration script for this platform now includes that person's recommendations.

I don't think it's realistic to expect that every platform provider will always have a staff member with Django deployment experience comparable to the strongest people in our community. Most of them are balancing their support for Django with support for Flask, Rails, JavaScript, Go, Rust, and many other languages and frameworks.

If `django-simple-deploy` continues to incorporate the feedback of the more experienced Django developers in the community, I could see platforms starting to incorporate the configuration steps that `django-simple-deploy` uses back into their own recommended best practices. This doesn't strike me as doing platforms' work for them; it seems to be an appropriate flow of information and experience between our community and platform hosts.

### There's no pressure to simplify the configuration for people

When we're writing a deployment tutorial, whether we're the platform host, an author, or a resource creator, we're often tempted to simplify the process. Every step we ask the user to take is a chance they'll make a typo or get off track somehow. So we're constantly balancing between supporting a well-architected deployment, and not making too many changes to the project.

By automating all the initial configuration, we can make any choices we want that support a good deployment. We can add as many config files as we want, set as many environment variables as needed, and run any followup commands we want. We're not limited to the bare-minimum "Getting Started" steps that you see in many platforms' onboarding docs. One simple example: we can generate well-commented config files, which are longer than a platform might want to present in their onboarding docs.

## Limitations

### Does not work for complex projects

`django-simple-deploy` aims to support projects that use a database, and involve user accounts. The current test project is a working blog project where users can make their own accounts and blogs. This project does not aim to support more complex projects that involve external services like email providers or payment workflows. This project has no ambition to support those kinds of Django projects.

### Does not work for click-based deployment processes

`django-simple-deploy` works well for deployment to platforms where the entire deployment process can be scripted through a CLI or an API. The project does not currently support deployment to platforms that require you to click through a web interface to configure a project, although it can help with some parts of that kind of process.

### May not work for projects that require an external hosting platform

`django-simple-deploy` aims to help you push projects from your local environment to a remote deployment environment. If a platform requires you to first push your project to an external hosting platform such as GitHub, `django-simple-deploy` can't currently mediate that process.

For platforms like this, `django-simple-deploy` may be able to configure projects for deployment. You would then be able to push your project to GitHub, and the rest of the platform's deployment process would work. The current priority is on platforms that don't require this intermediate step.
