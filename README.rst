======
README
======

Federation is an MMO turn based strategy game.


Introduction
------------

The code necessary to run a Federation server is located in the
directory called 'federation'. The Federation server provides the game
engine, a JSON API to interact with it, and a basic in-browser user
interface to the game. You do not need to download this code to play
Federation because your browser will automatically use the JavaScript
client when you visit the official website.

The 'tools' directory provides various tools used in the development
or maintenance of Federation.

The 'src' directory provides CoffeeScript files which are compiled
into JavaScript to be served by the server.

More information is available at the website: http://playfederation.com/


Python Dependencies
-------------------

+-------------+--------------------------+
| Package     | Website                  |
+=============+==========================+
| Python      | http://python.org/       |
+-------------+--------------------------+
| PyYAML      | http://pyyaml.org/       |
+-------------+--------------------------+
| Flask       | http://flask.pocoo.org/  |
+-------------+--------------------------+
| SQLAlchemy  | http://sqlalchemy.org/   |
+-------------+--------------------------+


Other Dependencies
------------------

+-------------+--------------------------+
| Package     | Website                  |
+=============+==========================+
| mod_wsgi    | http://modwsgi.org/      |
+-------------+--------------------------+
| node.js     | http://nodejs.org/       |
+-------------+--------------------------+
| CoffeScript | http://coffeescript.org/ |
+-------------+--------------------------+


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

To run Federation on a server, install Apache httpd and mod_wsgi and
configure your httpd.conf to use WSGI pointed at 'server.wsgi'.

You can also run a test instance of Federation on port 8080 with the
built in server technology of Flask. This is recommended for
development only; it is probably not robust enough for a public
server. To run Federation's test server, navigate to the Federation
directory and type:

    python test.py

Federation should 'just work' on any system that has Python and the
appropriate libraries installed. Python is an interpreted language, so
if you are missing a dependency, Federation will fail to serve up the
appropriate web pages, and there will be an error in the error
log. Make sure you have all of the dependencies installed before
running Federation!

Federation is heavily under development. It has only been tested under
recent versions of Fedora Linux with recent versions of the required
libraries. If Federation does not run, then it might require features
that are only in newer versions of the libraries that it uses. If you
have a way to find out the minimum required version of each
dependency, please tell us so we can add it to the dependency table
above. If additional code is needed for portability to other
platforms, contributions are welcome!


Legal
-----

The source code of this software is licensed under the MIT
license. For more information, see LICENSE.txt or go to:

    http://www.opensource.org/licenses/mit-license.php


FAQ
---

**Q**. Why do you require mod_wsgi?

**A**. Flask uses wsgi to talk to the production web server. We've only
tested Federation with Apache httpd. Thus, mod_wsgi for Apache httpd
is listed as a requirement. There is no guarantee that Federation will
work without modification on other web servers. For a list of all
servers which support wsgi, please see:

    http://wsgi.readthedocs.org/en/latest/servers.html
