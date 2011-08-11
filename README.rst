Backcap
=======

Backcap (Am.), to do one an ill-turn by speaking evil of 
him or carrying tales, or otherwise to "spoil his game." 

And that's what your users are going to do with you ! ;-)

What is backcap ?
=================

Backcap is a community-driven support module for any website.  

With it, users can post ideas, problems and questions to your support
team. People can vote for or against a feedback and you naturally see
what's important for your community.

In fact, that's something like an Help Center. And this is why we have
developped it, to provides a nice help center for the SpreadBand
website.

Features
========

For users:
- Post a feedback (from a plain page or a tab) -- question, idea, problem
- Browse and sort feedbacks
- Vote for or against a feedback
- Comment on a feedback
- Follow a feedback

For the staff:
- Assign a feedback to someone
- Set a state (Valid, Won't Fix, ...)
- Close, reopen, mark as duplicate, ...


Notifications are handled using django-notification and can be indexed
by haystack.


Requirements
============

Backcap requires:

- django-notifications
- django-voting

Backcap can make use of:

- haystack (for feedback indexing)
- south

Installation
============

1. Add 'backcap' directory to your PYTHON_PATH

2. Add 'backcap' to your INSTALLED_APPS in settings.py.

	INSTALLED_APPS = (
	    # ...
	    'backcap',
	    # ...
	)

3. Run syncdb and migrations

        $ ./manage.py syncdb
	$ ./manage migrate backcap

4. Write templates

5. You're done.




