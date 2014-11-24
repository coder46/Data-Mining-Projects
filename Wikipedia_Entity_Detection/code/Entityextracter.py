import re
import urllib
import urllib2
import string
import mechanize
import httplib2
import operator
import json
import math
from urlparse import urlparse
from bs4 import BeautifulSoup
from collections import OrderedDict

EntityType = {}

_digits = re.compile('\d')
def contains_digits(d):
    return bool(_digits.search(d))

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
			if Ename in EntityType:
				pass
			else:
				EntityType[Ename]={}
		elif line.strip()=="}}":
			pass
		else:
			key = line.split('=')[0].strip()
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

total_attrs= 0
def ParseFile():
	CNT = 0
	fileName = 'Out2.txt'
	
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
			try:
				name = 'RESULTS2/'+(str)(key)+'.txt'
				fo = open(name, 'wa')
				#print key
				#fo.write( (str)(value) )
				#l=[]
				no_of_ents = -1
				global total_attrs
				total_attrs = total_attrs + len(value.keys())
				for attr, vals in value.iteritems():
					#l.append(attr)
					if len(vals) > no_of_ents:
						no_of_ents = len(vals)
					info = {}
					info[1] = ''
					info[2] = ''
					info[3] = ''
					info[4] = -1
					info[5] = -1
					info[6] = []
					info[7] = 0
					info[1] = attr
					dats=[]
					num = int(float(max(1,math.ceil(math.log10(len(vals))))))
					dat_type={}
					dat_type["NUM"]=0
					dat_type["ALNUM"]=0
					dat_type["STR"]=0
					
					if len(vals) > 0:
						dats = vals[:(num)]
						for v in dats:
							if v.isdigit():
								dat_type["NUM"] = dat_type.get("NUM",0) + 1
							elif contains_digits(v):
								dat_type["ALNUM"] = dat_type.get("ALNUM",0) + 1
							else:
								dat_type["STR"] = dat_type.get("STR",0) + 1
					sorted_x = sorted(dat_type.items(), key=operator.itemgetter(1))
					info[2]=sorted_x[2][0]
					try:
						if info[2]=="NUM":
							vals = map(int, vals)
							vals.sort()
							info[4] = vals[0]
							info[5] = vals[len(vals)-1]
					except Exception, e:
						#print e
						pass

					info[7] = len(vals)
					#print info
					fo.write(json.dumps(info)+'\n')
				#print l	
				fo.write("Number of entities : " + str(no_of_ents) + "\n")
				fo.close()
				#print key, value
			except Exception, e:
				#print e
				pass

if __name__ == "__main__":
	ParseFile()
	print "Average number of attrs per entity type = " + str(float(total_attrs/len(EntityType.keys())))
