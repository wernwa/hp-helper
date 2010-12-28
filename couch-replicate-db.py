#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import re
import couchdb
import binascii
from time import time

couch = couchdb.Server('http://localhost:5984/')

try:
	dbname = sys.argv[1]
	raise Exception('spam', 'eggs')
except:
	print "usage: couch-replicate-db your-db-name"



# repliziere die zu online Datenbank
os.system('curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5984/_replicate -d \'{"source":"http://localhost:5984/'+dbname+'","target":"http://wernwa.couchone.com/'+dbname+'"}\'')



