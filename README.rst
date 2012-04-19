README
======

Federation is an MMO turn based strategy game.

More information is available at the website: http://playfederation.com/


Introduction
------------

The Federation server provides the game engine, a JSON API to interact
with it, and a basic in-browser user interface to the game. You do not
need to download this code to play Federation because your browser
will automatically use the JavaScript client when you visit the
official website.


Directory Layout
----------------

+----------------------+-------------------------------------------------+
| Directory            | Role                                            |
+======================+=================================================+
| federation           | A Python module that runs the Federation game.  |
+----------------------+-------------------------------------------------+
| federation/data      | All YAML configuration files that are used.     |
+----------------------+-------------------------------------------------+
| federation/static    | Static (i.e. unchanging) files that are served. |
+----------------------+-------------------------------------------------+
| federation/templates | HTML templates used by Flask.                   |
+----------------------+-------------------------------------------------+
| src                  | CoffeeScript source files to be compiled.       |
+----------------------+-------------------------------------------------+
| tools                | Small programs that supplement Federation.      |
+----------------------+-------------------------------------------------+


Python Dependencies
-------------------

+-------------+--------------------------------------+
| Package     | Website                              |
+=============+======================================+
| PyYAML      | http://pyyaml.org/                   |
+-------------+--------------------------------------+
| Flask       | http://flask.pocoo.org/              |
+-------------+--------------------------------------+
| SQLAlchemy  | http://sqlalchemy.org/               |
+-------------+--------------------------------------+
| Requests    | http://python-requests.org/          |
+-------------+--------------------------------------+
| PyExecJs    | http://pypi.python.org/pypi/PyExecJS |
+-------------+--------------------------------------+


Federation Clients
------------------

The source code here is only necessary to run a Federation
*server*. If you want to simply use a Federation *client* with an
existing server, then you can use any modern HTML 5 compliant browser
to play Federation. Internet Explorer does *not* currently work with
Federation because of incompatibilities and adding support for IE
browsers is very low priority.

This repository only contains the in-browser client and the test,
text-only client intended to be used by Federation developers. Other
clients, as they become available, will be located in different git
repositories so that you don't have to download all of the server
source code before you can run a client.


Running a Federation Server
---------------------------

Make sure to run ``setup.py`` before running Federation for the first
time! It compiles the src CoffeeScript into JavaScript and it imports
many of the Python dependencies so you'll have fewer surprises at
runtime. After ``setup.py`` works without issues, make sure that Flask
and SQLAlchemy are installed.

To run Federation on a server, install a WSGI-compatible server, such
as Apache with mod_wsgi, and point it at ``server.wsgi``. Currently,
only Apache has been tested with Federation.

You can also run a test server of Federation on port 8080 with the
built in server of Flask. Use this for development and testing, *NOT*
for a public server! Navigate to the Federation directory, or install
the federation package globally, and type:

    python -m federation

Federation is heavily under development. It has only been tested under
recent versions of Fedora Linux with recent versions of the required
libraries. If Federation does not run, please tell us so that we can
fix it! Be aware that the minimum version numbers for the dependencies
are not currently known.
