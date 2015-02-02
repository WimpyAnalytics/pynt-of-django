============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/WimpyAnalytics/pynt-of-django/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Pynt-of-django could always use more documentation, whether as part of the
official docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/WimpyAnalytics/pynt-of-django/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to let the code flow from your fingertips? Here's how to set up `pynt-of-django` for local development.

Get the code
~~~~~~~~~~~~

1. Fork the `pynt-of-django` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/pynt-of-django.git

Install Build Tool (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pynt-of-django uses it's own code to setup and manage the project.

    On Linux (one time) from the cloned dir::

        $ sudo pip install pynt

Install Dependencies
~~~~~~~~~~~~~~~~~~~~

System Packages
^^^^^^^^^^^^^^^
These are necessary for running tox. Which is required if you intend to make changes.

* Python dev package (python-dev on apt)
* Python 3 dev packages (python3-dev on apt)

Python Packages
^^^^^^^^^^^^^^^

Using build script::

    $ pynt create_venv

Making changes
~~~~~~~~~~~~~~

1. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

 Now you can make your changes locally. Make sure to periodically run the tests for the active Python and Django version::

   $ pynt test_nose

2. When you're done making changes, check that your changes work with all supported Python and Django versions::

    $ pynt test_tox

3. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

4. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, double check that existing documentation doesn't need updating.
3. The pull request should work for all supported Python and Django versions, and for PyPy. Check
   https://travis-ci.org/WimpyAnalytics/pynt-of-django/pull_requests
   and make sure that the tests pass for all configurations.