import re
import urllib
import urllib2
import string
import mechanize
import httplib2
from urlparse import urlparse
from bs4 import BeautifulSoup
from collections import OrderedDict

EntityType = {}

def isAlphamumeric( character ):
	if( character >= 'a' and character <= 'z' ):
		return 1
	if( character >= 'A' and character <= 'Z' ):
		return 1
	if( character >= '0' and character <= '9' ):
		return 1
	return 0

def isWhiteSpace( character ):
	if( character == ' ' or character == '\t' ):
		return 1
	return 0

def getEntityType( page ):
	start = 10
	index = 10
	entity = ""
	while( isAlphamumeric(page[index]) or isWhiteSpace(page[index]) ):
		entity = entity + page[index]
		index = index + 1
	entity = entity.strip()
	entity = entity.lower()
	if( entity in EntityType ):
		EntityType[entity] += 1
	else:
		EntityType[entity] = 1

def getEntityDets(infobox):
	Ename=""
	for line in infobox.splitlines():
		if line[:9]=='{{Infobox':
			Ename=line[10:].strip()
			Ename = '_'.join(Ename.split(' '))
			print Ename # NA
			if Ename in EntityType:
				pass
			else:
				EntityType[Ename]={}
		elif line.strip()=="}}":
			pass
		else:
			key = line.split('=')[0].strip()
			#print key # NEW ADDITION
			val = "NONE"
			try:
				val = line.split('=')[1].strip()
			except Exception, e:
				pass
			if key in EntityType[Ename]:
				pass
			else:
				EntityType[Ename][key]=[]
			if val in EntityType[Ename][key]:
				pass
			else:
				EntityType[Ename][key].append(val)
			
	#print Ename
	#print EntityType[Ename]

	

def clean_box(infobox):
	bracks = 0
	cbox = ""
	for i in range(len(infobox)):
			if infobox[i] == '{':
				try:
					if infobox[i+1] == '{':
						bracks = bracks + 2
				except Exception, e:
					pass
				cbox = cbox + infobox[i]
			
			elif infobox[i] == '}':
				try:
					if infobox[i+1] == '}':
						bracks = bracks - 2
				except Exception, e:
					pass
				cbox = cbox + infobox[i]
			
			elif infobox[i] == '[':
				try:
					if infobox[i+1] == '[':
						bracks = bracks + 2
				except Exception, e:
					pass
				cbox = cbox + infobox[i]
			
			elif infobox[i] == ']':
				try:
					if infobox[i+1] == ']':
						bracks = bracks - 2
				except Exception, e:
					pass
				cbox = cbox + infobox[i]
			
			elif infobox[i] == '(':
				bracks = bracks + 1
				cbox = cbox + infobox[i]
			
			elif infobox[i] == ')':
				bracks = bracks - 1
				cbox = cbox + infobox[i]
			
			elif infobox[i] == '|':
				if bracks == 2:
					cbox = cbox + "\n"
				else:
					cbox = cbox + '|'
			
			else:
				cbox = cbox + infobox[i]
	new_box = ""
	new_box = cbox[0]
	for i in range(1,len(cbox)):
		if cbox[i] == '\n' and cbox[i-1] == '\n':
			pass
		else:
			new_box = new_box + cbox[i]

	return new_box

def ParseFile():
	CNT = 0
	fileName = 'wiki.txt' # NEW ADDITION
	#fo = open('Out3.txt','w')
	with open(fileName) as f:
		page = ""
		brace_count = 0
		for line in f:
			#if CNT == 2:
			#	break
			if( line.find('{{Infobox') != -1 ):
				length = len(line)
				start = line.find('{{Infobox')
				i = start
				for i in range(start,length):
					if( line[i] == '{' and line[i+1] == '{'):
						brace_count = brace_count + 2
						page = page + line[i]
					elif ( line[i] == '}' and line[i+1] == '}'):
						brace_count = brace_count - 2
						page = page + line[i]
						if( brace_count == 0 ):
							#getEntityType(page)
							page = page + '}'
							getEntityDets(page)
							CNT = CNT + 1
							#fo.write(clean_box(page)+'\n')
							#fo.flush()
							page = ""
							break
					else:
						page = page + line[i]
				continue

			if( brace_count != 0 ):
				length = len(line)
				i = 0
				for i in range(0,length):
					if( line[i] == '{' and line[i+1] == '{' ):
						brace_count = brace_count + 2
						page = page + line[i]
					elif ( line[i] == '}' and line[i+1] == '}' ):
						brace_count = brace_count - 2
						page = page + line[i]
						if( brace_count == 0 ):
							#getEntityType(page)
							page = page + '}'
							getEntityDets(page)
							CNT = CNT + 1
							#fo.write(clean_box(page)+'\n')
							#fo.flush()
							page = ""
							break
					else:
						page = page + line[i]
		
		for key,value in EntityType.iteritems():
			name = 'entity/'+(str)(key)+'.txt'
			#fo = open(name, 'wa')
			#fo.write( (str)(value) )
			#fo.close()
			print key, value
		

if __name__ == "__main__":
	ParseFile()