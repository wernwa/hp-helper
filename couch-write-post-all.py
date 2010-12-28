#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import re
import couchdb
import binascii
from time import time

for file in os.listdir(sys.argv[1]):
	os.system('couch-write-post '+file)
