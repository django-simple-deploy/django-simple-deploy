"""A collection of messages used in deploy.py."""

# Storing messages here makes for a much shorter deploy.py file, and
#   makes it easier to see how the messages actually look on screen. The
#   disadvantage is that it's harder to track what messages are being
#   displayed when doing development work.
# When you add a message here, make sure the stdout.write() call has a comment
#   that clearly summarizes what the message says.
#
# Line length conventions
# - Try to keep lines at the 79-char PEP 8 limit, but the project is not
#   overly strict about it at this point.
#
# - DynamicMessages
#   - It can be helpful to make a second vertical line at 86 characters
#     (78 characters + two indentation levels) to judge the line lengths
#     for dynamic messages.


from textwrap import dedent

from django.conf import settings


cancel_automate_all = """
Okay, canceling this run. If you want to configure your project
for deployment, run the deploy command again without the --automate-all flag.
"""

unclean_git_status = """
The output of `git status` indicates that you have uncommitted changes.

We highly recommend you commit all changes before running the deploy command,
so you can easily undo configuration changes if deployment doesn't work, or if
you wish to deploy to a different platform.

Please commit all changes and then run the deploy command again. If you really
wish to continue without committing current changes, you can use
the --ignore-unclean-git flag.
"""

# Add-on to `unclean_git_status` when using automate-all.
unclean_git_automate_all = """
It's especially important to have a clean status when using the --automate-all
flag. In this case, django-simple-deploy will make commits on your behalf. It's a
really good idea to keep your commits separate from the commits that
django-simple-deploy makes.
"""


# --- Dynamic strings ---
# These need to be generated in functions, to display information that's
#   determined as the script runs.


# DEV: This should be updated for invalid plugin.
# def invalid_platform_msg(requested_platform):
#     """Error message, when an invalid --platform argument is provided."""

#     msg = dedent(
#         f"""

#         --- The platform "{requested_platform}" is not currently supported. ---

#         - Current options are: fly_io, upsun, and heroku
#         - Example usage:
#           $ python manage.py simple_deploy --platform fly_io
#           $ python manage.py simple_deploy --platform upsun
#           $ python manage.py simple_deploy --platform heroku

#     """
#     )
#     return msg


def file_found(filename):
    """Found a file that we plan to write.

    We need to get permission to write over this file. For example found an existing
    Dockerfile.
    """

    msg = dedent(
        f"""
        The file {filename} already exists. Is it okay to replace this file?
    """
    )
    return msg


def file_replace_rejected(filename):
    """Permission denied to replace existing file.

    We can't proceed without this permission.
    """

    msg = dedent(
        f"""
        In order to configure the project for deployment, we need to write the
        file: {filename}
        Please remove the current version, and then run the deploy command again.
    """
    )
    return msg
