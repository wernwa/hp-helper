#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import re
import couchdb
import binascii
from time import time




# open latex file
try:
    filename = sys.argv[1]
    in_file = open(filename,"r")
    text = in_file.read() #.encode('utf-8')
    in_file.close()
except:
    print "usage: replace-dollar-eqn your_latexfile.tex"
    exit(1)

# find $$ in 
p = re.compile('\$\$(.*?)\$\$',re.DOTALL)
text = p.sub('\\[\\1\\]',text)

# find inline $
p = re.compile('\$(.*?)\$',re.DOTALL)
text = p.sub('\\(\\1\\)',text)

#filename = filename + ".eqn.tex"
eqn_file = open(filename,"w")
eqn_file.write(text)
eqn_file.close()


