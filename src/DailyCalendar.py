#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ics import Calendar, Event
import os

import locale
locale.setlocale(locale.LC_TIME, "")

from ics.event import Event
from ics.timeline import Timeline
from ics.icalendar import Calendar
from ics.parse import string_to_container

from datetime import datetime
from urllib2 import urlopen
import arrow


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont   

pdfmetrics.registerFont(TTFont('Robo_light', './ttf/RobotoCondensed-Light.ttf'))
pdfmetrics.registerFont(TTFont('Robo_reg', './ttf/Roboto-Regular.ttf'))


date = arrow.Arrow(2017, 7, 1, 22)
date2 = arrow.Arrow(2017, 8, 18, 5)

blacklist = ["13nrad4g7hjjv8omig8vvitjcc@google.com"]

url = "https://calendar.google.com/calendar/ical/3fo3jbnh8fq15h3g59uakeiv6s%40group.calendar.google.com/private-15cbb7aa831a14d137b0d151b697929e/basic.ics"
c = Calendar(urlopen(url).read().decode('utf8'))

date.humanize(locale='cs')
#day_events = c.timeline.overlapping(date, date2)
day_events = c.timeline.included(date, date2)
#day_events = c.timeline
#print day_events
#print len(day_events)

icons = {
	'Snídaně': './icon/fork.png',
	'Oběd': './icon/fork.png',
	'Večeře': './icon/fork.png',
	'Půlnočka': './icon/fork.png',
}

def paticka(pdf):
	pdf.setFont('Robo_reg', 2)
	pdf.setFont('Robo_reg', 8)
	pdf.drawString(10,30,"V programu může dojít ke změnám. Aktuální verze programu je v online verzi dynamického programu.")
	pdf.drawString(10,21,"V případě špatného počasí bude místo pozorování vymyšlen náhradní program. Pozorování je možné prodloužit po dohodě s vedoucím")
	pdf.setFont('Robo_light', 7)
	pdf.drawString(10,5,"Tento program byl vygenerován automaticky %s na základě expedičního dynamického programu, Astronomická Expedice 2017, Roman Dvořák, DailyCalendar.py, v0.2" %(arrow.now().strftime('%d.%m.%Y v %H:%M')))
	
	pdf.drawImage("qr_gcal.jpg", 450, 80, 100, 100)
	pdf.setFont('Robo_light', 10)
	pdf.drawString(460,83,"Online verze programu")
	pdf.drawString(460,73,"http://goo.gl/WCkXKv")

def hlavicka(pdf):

	pdf.showPage()
	pdf.setLineWidth(.3)
	pdf.setFont('Robo_light', 24)
	pdf.drawString(80,790,"Astronomická expedice Úpice 2017")
	pdf.setFont('Robo_reg', 24)
	pdf.drawString(80,790-28,"Denní program")
	pdf.setFont('Robo_light', 12)
	pdf.line(80,760,600,760)
	pdf.line(80,758,600,758)

def udalost(pdf, event):
	height = 35
	print "~~~~~~~~~~~~~~~~~~~"
	begin = event.begin.to('Europe/Prague')
	end = event.end.to('Europe/Prague')
	name = event.name
	location = event.location
	color = event.color
	description = event.description
	print name
	pdf.setFont('Robo_reg', 2)

	icons = {
		'Snídaně': './icon/fork.png',
		'Oběd': './icon/fork.png',
		'Večeře': './icon/fork.png',
		'Půlnočka': './icon/fork.png',
		'Budíček': './icon/alarm_grey_192x192.png',
		'Přelet': './icon/satellite-xxl.png',
		'Táborák': './icon/feedburner-xxl.png',
		'pozorování': './icon/telescope.png',
		'Zpracování': './icon/pencil.png',
		'Příprava': './icon/tool-box-xxl.png',
		'event': './icon/today-xxl.png',
	}

	print name.encode('UTF-8').split(" ")[0]

	if name.encode('UTF-8').split(" ")[0] in icons:
		pdf.drawImage(icons[name.encode('UTF-8').split(" ")[0]], 55, page-3, 15, 15)
	else:
		pdf.drawImage(icons['event'], 55, page-3, 15, 15)

	pdf.setFont('Robo_light', 4)
 	#pdf.drawString(50,page, str(event.uid))
	pdf.setFont('Robo_reg', 12)
	pdf.drawString(75,page, name)
	pdf.setFont('Robo_light', 9)
	if begin == end:
		pdf.drawString(100,page - 12, "(" + begin.strftime('%H:%M') + ")    "+ location  )
	else:
		pdf.drawString(100,page - 12, "(" + begin.strftime('%H:%M') + " - " + end.strftime('%H:%M') + ")    "+ location)
	pdf.setFont('Robo_light', 9)
	l_desc = len(description)
	print l_desc
	if l_desc == 0:
		height += 0
	elif l_desc < 150:
		height += 10
		pdf.drawString(100,page - 25, description )
	elif l_desc < 500:
		height += 20
		pdf.drawString(100,page - 25, description )
	#pdf.setFont('Robo_light', 4)
 	#pdf.drawString(50,page-40, str(event.uid))


	return height


pdf = canvas.Canvas("program.pdf")
page = 700
day = arrow.Arrow(2017, 01, 01)
for i, event in enumerate(day_events):
	begin = event.begin.to('Europe/Prague')

	#if begin > date:
	if not event.uid in blacklist:
	#if True:
		try:
			if begin > day:
				hlavicka(pdf)
				paticka(pdf)
				page = 700
				print ""
				print "NOVY DEN"

				pdf.setFont('Robo_light', 14)
				pdf.drawString(300,page+35, "Program na "+ begin.format('dddd', locale="cs") + day.strftime('   (%D)'))
				day = begin.replace(days=+1, hour=5, minute=0)
				print begin

				print "===================================="
			page -= udalost(pdf, event)
			#page -= 55
			if page <= 70:
				pdf.showPage()
				paticka(pdf)
				page = 800
		except Exception as e:
			print "Err >>", repr(e)
	else:
		print "out of range !!!!!!!!!!!!!!!!!!!!!!!!!!!", event.name

pdf.save()
print "done"

'''

for a in range(0, 20):
	ev = c.events[a]
	print ev.color
	print ev.duration
	print ev.end
	print type(ev.__str__)
	print ev.created
	print "###################"
'''