---
title: Unit Tests
hide:
    - footer
---

Even as `django-simple-deploy` reaches the 1.0 release, the internal codebase is steadily evolving. Unit tests should be written only for the following:

- Specific functions and methods that are critical to current behavior;
- Functions and methods that are likely to be stable for multiple major releases.
- If someone reports a bug, or you find one, definitely consider writing a unit test that prevents that bug from reappearing.

For all unit tests, try to write them in a way that they're not overly dependent on implementation. If you need to change the structure of the project to support that, feel free to suggest that change. For example there's probably a good deal of functionality that can be moved out of a class and into a utility function that's easier to test in isolation.

Running unit tests
---

```sh
(.venv)django-simple-deploy$ pytest tests/unit_tests
```

This will run unit tests for the core `django-simple-deploy` project, and for a plugin that's installed in editable mode.

Running unit and integration tests together
---

Unit tests and integration tests can be run together:

```sh
(.venv)django-simple-deploy$ pytest
```

The bare `pytest` command will run all unit and integration tests for the core `django-simple-deploy` project, and for a plugin that's installed in editable mode. It will *not* run end-to-end tests; those tests need to be run explicitly.