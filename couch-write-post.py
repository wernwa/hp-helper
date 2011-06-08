#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import re
import couchdb
import binascii
from time import time

#couch = couchdb.Server('http://localhost:5984/')
couch = couchdb.Server('http://wernwa:init10@wernwa.couchone.com/')

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


param['id'] = filename.replace('.html','');


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


# some error handling
try:
	param['db']
except:
	print "Error: %couchdb db=<the_db> is needed for creating the document in the couchdb"
try:
	param['tags']
except:
	param['tags']=[]




# lösche komentare
param['posthtml'] = re.sub('(<!--.*-->)','',param['posthtml']);

# hänge latex falls existent als kommentar an posthtml für die Suche
if 'texpath' in param:
	try:
		fh = open(param['texpath'],'r')
		param['latex'] = fh.read().decode('utf-8')
		fh.close()
	except:
		print ''
		#param['latex'] = ''
	
	#param['latex'] = re.sub('-->','',param['latex']);
	#param['posthtml'] = param['posthtml']  + '<!--'+param['latex']+'-->'



db = couch[param['db']]


# update the document
b_created_now = False
if not param['id'] in db:
	print "erstelle ein neues dokument '"+param['id']+"'"
	db[param['id']] = {'creation':int(time()), 'type':'article', 'tags':param['tags'], 'posthtml':param['posthtml']}
	b_created_now = True

doc = db[param['id']]
doc['tags']=param['tags']
doc['posthtml'] = param['posthtml']
if 'latex' in param:
	doc['latex'] = param['latex']
if not b_created_now:
	doc['changed']=int(time())
	print 'versuche "'+param['id']+'" zu aktualisieren...'
try:
	db[param['id']] = doc
	print 'dokument '+param['id']+' aktualisiert'
except:        
	print 'es sind Fehler aufgetreten'
	print StandardError.str()
	exit(1)

    





# repliziere die zu online Datenbank
#replicate_b = raw_input('----- locale Datenbank replizieren? (j/[n]) ')
#if replicate_b == 'j':
#	os.system('curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5984/_replicate -d \'{"source":"http://localhost:5984/'+param['db']+'","target":"http://wernwa.couchone.com/'+param['db']+'"}\'')



