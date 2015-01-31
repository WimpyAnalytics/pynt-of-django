pynt-of-django
==============

This library provides a set of pre-built tasks for your, pynt based,
build.py along with supporting utility and project specific functions.

|Build Status|

Install
-------

-  ``pip install pynt-of-django``

Usage
-----

From within your build.py, setup pyntofdjango.

::

    import os
    import pyntofdjango
    pyntofdjango.setup_pod(os.path.abspath(__file__))

Import any tasks you may need. See `pyntofdjango's
build.py <https://github.com/WimpyAnalytics/pynt-of-django/blob/master/build.py>`__
for a full list.

::

    from pyntofdjango.tasks import create_venv, manage, test_nose

Now you should see your new tasks on the command line.

::

    pynt -l

About
-----

This project builds on the `basic way to use
virtualenv <http://docs.python-guide.org/en/latest/dev/virtualenvs/#basic-usage>`__,
where the virtualenv folder (called venv) is placed within the project
and ignored by the repo.

Why an in-project virtualenv?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The most important bit is that it allows devs to get going with your
project without worrying about virtualenv all the time. There are more
reasons and there are disadvantages. `Christopher Webber has an
explitive filled
presentation <http://pyvideo.org/video/1870/in-project-virtualenvs>`__
on some of the reasons in-project virtualenvs may be your style.

Why not use [my favorite build tool]?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Pynt <https://github.com/rags/pynt>`__ is very simple but nice for that
same reason.

1. It's pure Python and as a result it works great on all platforms.
2. It's only a local build tool and not a deployment tool and neither is
   this project.
3. It supports Python 3 and so does this project.
4. It makes for a cool companion project name.

.. |Build Status| image:: https://travis-ci.org/WimpyAnalytics/pynt-of-django.svg?branch=master
   :target: https://travis-ci.org/WimpyAnalytics/pynt-of-django
