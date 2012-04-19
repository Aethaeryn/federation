# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

'''Runs a test server locally on port 8080 via Flask's built in server
functionality. Do *NOT* use this in a production environment. Instead
of executing the federation module directly, point a wsgi-compatible
server at server.wsgi, which is included in the parent directory.
'''
from federation import app as application

application.run(host='0.0.0.0', port=8080)
