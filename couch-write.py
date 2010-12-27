#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import re
import couchdb
import binascii
from time import time

couch = couchdb.Server('http://localhost:5984/')




# open latex file
try:
	filename = sys.argv[1]
	in_file = open(filename,"r")
	latex = in_file.read().decode('utf-8')
	in_file.close()
except:
	print "usage: couch-write your_latexfile.tex"
	exit(1)

# find parameters in the latex-file
p = re.compile('\%couchdb (.*)')
mlist = p.findall(latex)
param = {}

for m in mlist:
	print m
	part = m.partition('=')
	if part[0] == 'tags':
		param[part[0]] = part[2].split(',');
	else:
		param[part[0]] = part[2]

# lade post html
filepost = filename.replace('.tex','.post.html')
try:
	fh = open(filepost,'r')
	param['posthtml'] = fh.read().decode('utf-8')
	fh.close()
except:
	print "note: keine post.html datei"
	param['posthtml'] = ""


    
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
	doc['latex'] = latex
	doc['type']='article'
	doc['tags']=param['tags']
	doc['pdflink']=param['pdflink']
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
	db[param['id']] = {'latex': latex, 'creation':int(time()), 'type':'article', 'tags':param['tags'], 'pdflink':param['pdflink'], 'posthtml':param['posthtml']}
    




#db.delete(db['delme'])


#curl -vX PUT http://127.0.0.1:5984/albums/6e1295ed6c29495e54cc05947f18c8af/ artwork.jpg?rev=2-2739352689 --data-binary @artwork.jpg -H "Content-Type: image/jpg"

"""
# find images in the latex-file
p = re.compile('\\includegraphics\[.*?\]\{(\w+\.\w+)\}',re.MULTILINE)
mlist = p.findall(latex)
for m in mlist:
    try:
        fh = open(m,'r')
        #in_file = open(m,"r")
    except:
        print m+" existiert nicht"
        continue

    #print m+" wird hochgeladen..."     
    
    db = couch[param['db']]
    doc = db[param['id']]
    #db.put_attachment(db[param['id']],binascii.b2a_base64(fh.read()),m)
    #fh.close()

    cmd = "curl -X PUT http://127.0.0.1:5984/physik/"+doc['_id']+"/"+m+"?rev="+doc['_rev']+" --data-binary @"+m+" -H \"Content-Type: image/png\""

    if '_attachments' in doc and m in doc['_attachments']:
        print m+" bereits gespeichert ",
        upload_b=raw_input('überschreiben? (j/[n]) ')

        if upload_b=='j':
            print m+" wird hochgeladen..."     
            os.system(cmd) 
    else:
        print m+" wird hochgeladen..."  
        os.system(cmd)



# lade die pdf Datei hoch
filepdf = filename.replace('.tex','.pdf')
try:
    fh = open(filepdf,'r')
    doc = db[param['id']]
    cmd = "curl -X PUT http://127.0.0.1:5984/physik/"+doc['_id']+"/"+doc['_id']+".pdf?rev="+doc['_rev']+" --data-binary @"+filepdf+" -H \"Content-Type: application/pdf\""
    os.system(cmd)
    print "lade pdf Datei"
except:
    print "bitte pdf Datei erzeugen"

"""



# repliziere die zu online Datenbank
replicate_b = raw_input('----- locale Datenbank replizieren? (j/[n]) ')
if replicate_b == 'j':
	os.system('curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5984/_replicate -d \'{"source":"http://localhost:5984/'+param['db']+'","target":"http://wernwa.couchone.com/'+param['db']+'"}\'')
