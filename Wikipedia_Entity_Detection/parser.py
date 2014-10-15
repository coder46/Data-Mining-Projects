import re
from BeautifulSoup import BeautifulSoup, SoupStrainer

f = open('/media/faisal/705EE92D2E9CD9FC/Users/faisal-pc/IIIT/WebMining/Assignment4/dataset/wikifile.xml','r')

flag = 0
page_info=""
count = 0
'''
for line in f:
	if count == 100:
		break
	if line.strip() == "<page>":
		page_info = ""
		flag = 1
		page_info = page_info + line
	elif line.strip() == "</page>":
		count = count + 1
		page_info = page_info + line
		#print page_info
		flag = 0
		soup = BeautifulSoup(page_info)
		print soup.find('table',attrs={'class':'infobox'})
		print "\n"
	else:
		if flag == 1:
			page_info = page_info + line
 '''
'''
for line in f:
	#if count == 200:
	#	break
	#if line.strip()[:9] == "{{Infobox":
	if re.search("{{Infobox",line.strip()):
		page_info = ""
		flag = 1
		page_info = page_info + line
	else:
		if flag == 1:
			if re.search("}}",line):
				count = count + 1
				page_info = page_info + line
				#print page_info
				flag = 0
				print page_info
				page_info = ""
			else:
				page_info = page_info + line
 

f.close()
'''
'''
elif line.strip() == "}}" or line.strip() == "|}}":
	if flag == 1:
		count = count + 1
		page_info = page_info + line
		#print page_info
		flag = 0
		print page_info
		page_info = ""
		print "\n"
'''
bracks = 0
for line in f:
	if line[0:9] == "{{Infobox":
		page_info = ""
		#bracks = 0
		flag = 1
		#page_info = page_info + line
		for i in range(len(line)):
			if line[i]=='{':
				if flag == 1:
					bracks = bracks + 1
					page_info = page_info + line[i]
			elif line[i]=='}':
				if flag == 1:
					bracks = bracks - 1
					page_info = page_info + line[i]
					if bracks == 0:
						count = count + 1
						flag = 0
						print page_info
						page_info = ""
						break
			else:
				if flag == 1:
					page_info = page_info + line[i]
		
	else:
		if flag == 1:
			for i in range(len(line)):
				if line[i]=='{':
					if flag == 1:
						bracks = bracks + 1
						page_info = page_info + line[i]
				elif line[i]=='}':
					if flag == 1:
						bracks = bracks - 1
						page_info = page_info + line[i]
						if bracks == 0:
							count = count + 1
							flag = 0
							print page_info
							page_info = ""
							break
				else:
					if flag == 1:
						page_info = page_info + line[i]

f.close()