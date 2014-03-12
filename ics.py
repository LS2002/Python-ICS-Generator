# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from time import gmtime, strftime,localtime

from datetime import datetime, timedelta
#import requests
import time
import urllib2
import re


url_states = "http://gunshowtrader.com/gun-shows/"


def getContent(url):
	html_page = urllib2.urlopen(url).read()
	return BeautifulSoup(html_page)


def getStates(bs4_content):
	
	for state in bs4_content.find("section", attrs={"class":"widget widget_gst_sidebar_states"}).findAll("li"):
		url_state = state.find('a').get('href')
		time.sleep(3)
		content_state = getContent(url_state)
		getList(state.string, content_state) #pass state name
		# break;
		

def getList(catstr, bs4_content):
	for allcontent in bs4_content.findAll("tr",attrs={"class":['dark','light']}):
		time = allcontent.findAll("time")
		link = allcontent.find("a",attrs={"itemprop":"url"}) 
		if(len(time)==1):
			endDate = datetime.strptime(time[0].get('datetime'), "%Y-%m-%d") + timedelta(days=1)
		if(len(time)==2):
			endDate = datetime.strptime(time[1].get('datetime'), "%Y-%m-%d") + timedelta(days=1)

		saveEventToICS(time[0].get('datetime'), endDate.strftime("%Y-%m-%d"), link.get('href'), link.get('title'))
		print time[0].get('datetime') + " " + endDate.strftime("%Y-%m-%d") + " " + link.get('title') + " " + link.get('href')


def trimDateFormat(date):
	theDate = date.split("-")
	return theDate[0]+theDate[1]+theDate[2]

def saveEventToICS(start, end, desc, name):
	finalstring  = "\nBEGIN:VEVENT"
	finalstring += "\nDTSTART;VALUE=DATE:"+trimDateFormat(start)
	finalstring += "\nDTEND;VALUE=DATE:"+trimDateFormat(end)
	finalstring += "\nDESCRIPTION:"+desc
	finalstring += "\nLOCATION:\nSEQUENCE:0\nSTATUS:CONFIRMED"
	finalstring += "\nSUMMARY:"+name
	finalstring += "\nTRANSP:TRANSPARENT\nEND:VEVENT"
	saveToICS(finalstring)

def saveToICS(finalstring):
	f = open(ics_file_name,'a')
	f.write(finalstring.encode('utf-8'))

def initICS():
	finalstring = "BEGIN:VCALENDAR\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:Gunshow\nX-WR-TIMEZONE:America/Los_Angeles"
	saveToICS(finalstring)

def closeICS():
	finalstring = "\nEND:VCALENDAR"
	saveToICS(finalstring)

#=======================================================================
ics_file_name = strftime("GunShow_%Y-%m-%d_%H-%M-%S", localtime()) + ".ics"
initICS()
getStates(getContent(url_states))
closeICS()
