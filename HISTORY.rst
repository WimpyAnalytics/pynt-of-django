.. :changelog:

History
-------

0.3.2 (2018-02-09)
------------------

* Removed Django installation requirement

0.3.1 (2018-02-09)
------------------

* Fixed issue with manage.py being found in .tox

0.3.0 (2015-08-07)
------------------

* Most commands wrapping an underlying executable now accept both positional and named (--foo=bar) shell arguments.
* create_venv now uses --no-site-packages for venv by default
* test_tox is working again
* clean works again, also cross platform compliant
* Now using pyntcontrib functions where possible

0.2.0 (2015-02-01)
------------------

* test_* and manage related tasks now pass along args to underlying commands.
* For safety: delete_venv task now refuses to delete a dir larger than a max of ~500mb

0.1.0 (2014-11-16)
------------------

* First release on PyPI.
