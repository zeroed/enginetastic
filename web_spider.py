from datetime import datetime
from urlparse import urlparse
import random
import urllib2
import re

""" 
:: PY WEB CRAWLER ::

	- parametro in input: un indirizzo web.
	- il crawler scansiona la pagina data ed isola
		- nome del dominio di primo livello
		- titolo della pagina dall'header
		- link contenuti nella pagina
	- memorizza in una struttura dati:
		- le URL visitate
		- le URL contenute nella pagina
		- il titolo della pagina
		- il timestamp del collegamento
		- la favicon
	- riconosce i loop
	- opzionalmente recupera alcune informazioni dal servizio di WhoIS o di DNS
	- sceglie a caso un indirizzo e salta
	- il crawler dovrebbe essere in grado di individuare le URL esterne e prediligerle a quelle interne
	- opzionalmente il crawler dovrebbe eseere in grado i fare backtrack in caso di vicoli cieci
	- il crawler memorizza le informazioni che raccoglie su un database
"""
"""
	 http://love-python.blogspot.com/2010/09/python-code-to-retrive-links-from-web.html
	 http://docs.python.org/library/urllib2.html
	 http://docs.python.org/library/urlparse.html
	 
	 http://docs.python.org/library/urllib.html
	 http://docs.python.org/library/urlparse.html
	 http://docs.python.org/library/urlparse.html  <--
"""

def get_hyperlinks(url,data):	
	if url.endswith("/"):
		url = url[:-1]	
	#Compile a regular expression pattern into a regular expression object, which can be used for matching
	urlpat = re.compile(r'<a [^<>]*?href=("|\')([^<>"\']*?)("|\')')
	#(r'<a [^<>]*?href=("|\')([^<>"\']*?)("|\')') 
	#Find all substrings where the RE matches, and returns them as a list.
	result = re.findall(urlpat, data)
	parselist = []
	urlist = []
	suburllist = []	
	for item in result:
		link = item[1]		
		o = urlparse(link)
		parselist.append("[scheme]"+o.scheme+"[netlock]"+o.netloc+"[path]"+o.path)				
		if link.startswith("http://") and link.startswith(url):
			if link not in suburllist:
				suburllist.append(link)
		elif link.startswith("http://") and not link.startswith(url):
			if link not in urlList:
				urllist.append(link)		
		elif link.startswith("https://") :
			#if link not in urlList:
			#	urlList.append(link)
			pass				
		elif link.startswith("/"):
			link = url + link
			if link not in suburllist:
				suburllist.append(link)
		"""
		else:
			link = url + "/" + link
			if link not in urllist:
				urllist.append(link)
		else:
			link = url + "/" + link
			if link not in urllist:
				urllist.append(link)
		"""
	print "urllist len: "+str(len(urllist))
	print "suburllist len: "+str(len(sublrllist))	
	return urllist

def get_jump_list(url,data):
	if url.endswith("/"):
		url = url[:-1]	
	#Compile a regular expression pattern into a regular expression object, which can be used for matching
	urlPat = re.compile(r'<a [^<>]*?href=("|\')([^<>"\']*?)("|\')')
	#(r'<a [^<>]*?href=("|\')([^<>"\']*?)("|\')') 
	#Find all substrings where the RE matches, and returns them as a list.
	result = re.findall(urlPat, data)
	jumplist = []
	for item in result:
		link = item[1]		
		o = urlparse(link)
		target = o.scheme+"://"+o.netloc
		if target.startswith("http://") and not target.startswith(url):
			if target not in jumplist:
				jumplist.append(target)
	print "jumplist len: "+str(len(jumplist))
	return jumplist

def show_list(urllist):
	urllist.sort()
	for x in range(len(urllist)):
		print "["+str(x)+"] "+urllist[x]
		o = urlparse(urllist[x])
		print("[scheme]"+o.scheme+"[netlock]"+o.netloc+
		"[path]"+o.path+"[params]"+o.params+
		"[query]"+o.query+"[fragment]"+o.fragment)
		print "---------"

def url_grab(url):
	if not url.startswith("http://"):
		url = "http://"+url
	usock = urllib2.urlopen(url)
	data = usock.read()
	usock.close()
	return data

def choose_destination(urllist, starturl, last):
	x = random.randint(0,len(urllist)-1)
	target = urllist[x]
	print "next jump to: "+target
	return target
	
def get_single_url_list():
	print "Enter the URL: "
	url = raw_input("> ")
	data = url_grab(url)
	#urllist = get_hyperlinks(url, data)
	urllist = get_jump_list(url, data)
	show_list(urllist)
	choose_destination(urllist)
	
def engine(starturl):
	count = 1
	jump = starturl
	last = starturl
	path = []
	path.append(jump)
	while count<20:
		last = jump
		data = url_grab(jump)
		urllist = get_jump_list(jump, data)
		if len(urllist)==0:
			jump=starturl
		else:
			jump = choose_destination(urllist, starturl, last)
		path.append(jump)
		print "running"
		count+=1
	print "run end"
	show_list(path)
	string = ""
	for item in path:
		string = string + " - "+item
	return string












