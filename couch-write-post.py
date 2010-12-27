#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import re
import couchdb
import binascii
from time import time

couch = couchdb.Server('http://localhost:5984/')


param = {}

# lade post html
try:
	filename = sys.argv[1]
	fh = open(filename,'r')
	param['posthtml'] = fh.read().decode('utf-8')
	fh.close()
except:
	print "usage: couch-write-post your_html.html"
	param['posthtml'] = ""


# find parameters in the html-file
p = re.compile('<!--couchdb (.*)-->')
mlist = p.findall(param['posthtml'])


for m in mlist:
	print m
	part = m.partition('=')
	if part[0] == 'tags':
		param[part[0]] = part[2].split(',');
	else:
		param[part[0]] = part[2]


try:
	param['db']
except:
	print "Error: %couchdb db=<the_db> is needed for creating the document in the couchdb"


try:
	param['id']
except:
	print "Error: %couchdb id=<the_doc_id> is needed for creating the document in the couchdb"

try:
	param['tags']
except:
	param['tags']=[]


db = couch[param['db']]


# update the document
#try:
if param['id'] in db:
	doc = db[param['id']]
	doc['type']='article'
	doc['tags']=param['tags']
	doc['changed']=int(time())
	doc['posthtml'] = param['posthtml']
	print 'versuche "'+param['id']+'" zu aktualisieren...'
	try:
		db[param['id']] = doc
		print 'dokument '+param['id']+' aktualisiert'
	except:        
		print 'es sind Fehler aufgetreten'
		print StandardError.str()
		exit(1)
# if not exists, create new
#except:
else:
	print "erstelle ein neues dokument '"+param['id']+"'"
	db[param['id']] = {'creation':int(time()), 'type':'article', 'tags':param['tags'], 'posthtml':param['posthtml']}
    





# repliziere die zu online Datenbank
replicate_b = raw_input('----- locale Datenbank replizieren? (j/[n]) ')
if replicate_b == 'j':
	os.system('curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5984/_replicate -d \'{"source":"http://localhost:5984/'+param['db']+'","target":"http://wernwa.couchone.com/'+param['db']+'"}\'')



