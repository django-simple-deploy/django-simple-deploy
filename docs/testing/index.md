---
title: Testing
hide:
    - footer
---

Testing is somewhat complex for `django-simple-deploy`, because it's a standalone management command that acts on a separate Django project. It's not a full Django project, so it lacks a lot of the infrastructure that's typically used for testing.

This affects integration and e2e tests most significantly. Those tests need to create a Django project in a temp directory, and run the `deploy` command against that project. I'm sure there are numerous ways to simplify the current approach to testing, but the current approach is serving to support ongoing development.

If you have questions about how to run tests, or feedback on how to simplify the test suite, please share it!