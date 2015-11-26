#!/usr/bin/python
# -*- coding: utf-8 -*-

# NOTE: requires wget command

import os,sys

fn = 'nwsdata.txt'
stationid = "xxxMTRggw"
logging = True

#     Project: tmp.py
#      Author: fyngyrz  (Ben)
#     Contact: fyngyrz@gmail.com (bugs, feature requests, kudos, bitter rejections)
#     Project: slacker.py
#    Homepage: https://github.com/fyngyrz/slacker
#  Depends on: NWS web services
#     License: None. It's free. *Really* free. Defy invalid social and legal norms.
# Disclaimers: 1) Probably completely broken. Do Not Use. You were explicitly warned. Phbbbbt.
#              2) My code is blackbox, meaning I wrote it without reference to other people's code
#              3) I can't check Other People's Code effectively, so if you use any version
#                 of this that incorporates accepted commits from others, you are then risking
#                 the dangers of OPC, as *well* as risking the use of my code. Using OPC
#                 *also* means you will be using code that may or may not be protected by
#                 copyright, patent, and the like, because our intellectual property system
#                 is pathological. All risks and responsibilities and any subsequent
#                 consequences of this are entirely yours. Have you written your congresscritter
#                 about patent and copyright reform yet?
#  Incep Date: November 24th, 2015
#     LastRev: November 25th, 2015
#  LastDocRev: November 25th, 2015
# Tab spacing: 4 (set your editor to this for sane formatting while reading)
#     Dev Env: Ubuntu 12.04.5 LTS, Python 2.7.3, Apache2
#  Also works: OS X 10.6.8
#      Status: BETA
#    Policies:  I will make every effort to never remove functionality or
#               alter existing functionality once past BETA stage. Anything
#               new will be implemented as something new, thus preserving all
#               behavior and API. The only intentional exceptions to this
#               are if a bug is found that does not match the intended behavior,
#               or I determine there is some kind of security risk. What I
#               *will* do is not document older and less capable versions of a
#               function, unless the new functionality is incapable of doing
#               something the older version(s) could do. Remember, this only
#               applies to production code. Until the BETA status is removed,
#               ANYTHING may change. Also, read "Disclaimers", above. Then
#               read it again. Note that while production code as I define it
#               will be more stable, that doesn't imply in any way that it is
#               more, or even at all, reliable. Read "Disclaimers", above. Did
#               I mention you should read the disclaimers? Because you know,
#               you really should. Several times. Read the disclaimers, that is.

# Here's what is in the typical NWS data chunk we're fetching:
# ============================================================
#       +- Day of month
#       | +- 2-digit Hour
#       | | +- 2-digit minute
#       | | |+- Zulu time indicator
#       | | ||    +- Automated, no observer
#       | | ||    |   +- Wind direction, degrees (0 is true north)
#       | | ||    |   | +- Wind speed is... Knots
#       | | ||    |   | |  +- Wind gusting to... Knots
#       | | ||    |   | |  |     +- No clouds below 12,000 AGL
#       | | ||    |   | |  |     |   +- (M)inus temperature, Celsius
#       | | ||    |   | |  |     |   |   +- (M)inus temperature, Celsius, Dewpoint
#       | | ||    |   | |  |     |   |   |     +- Altimeter
#       | | ||    |   | |  |     |   |   |     |   +- Site has a precip sensor (A01, not)
#       | | ||    |   | |  |     |   |   |     |   |  +- (Peak...
#       | | ||    |   | |  |     |   |   |     |   |  |   +- Wind) in last hour
#       | | ||    |   | |  |     |   |   |     |   |  |   |   +- Wind direction, degrees (0 is true north)
#       | | ||    |   | |  |     |   |   |     |   |  |   |   | +- 38 Knots
#       | | ||    |   | |  |     |   |   |     |   |  |   |   | |    +- Zulu time of peak
#       | | ||    |   | |  |     |   |   |     |   |  |   |   | |    |   +- Sea Level Pressure
#       | | ||    |   | |  |     |   |   |     |   |  |   |   | |    |   |  +- (10)12.5 MB
#       | | ||    |   | |  |     |   |   |     |   |  |   |   | |    |   |  |  +- 1=minus,0=plus
#       | | ||    |   | |  |     |   |   |     |   |  |   |   | |    |   |  |  |  +- 2.2c temperature
#       | | ||    |   | |  |     |   |   |     |   |  |   |   | |    |   |  |  |  |+ 1=minus,0=plus
#       | | ||    |   | |  |     |   |   |     |   |  |   |   | |    |   |  |  |  ||  +- 14/4c dewpoint
#       | | ||    |   | |  |     |   |   |     |   |  |   |   | |    |   |  |  |  ||  |
# KGGW 190053Z AUTO 29022G30KT CLR M02/M14 A2983 AO2 PK WND 30038/0003 SLP125 T10221144

# Go get the NWS data:
# --------------------
t = 'wget -q -O %s "http://www.wrh.noaa.gov/total_forecast/getprod.php?toggle=textonly&afos=%s"' % (fn,stationid)
os.system(t)
fh = open(fn)
da = fh.read()
fh.close()

# Now clean it up. No pre tags, no linefeeds, no leading/trailign white space
# ---------------------------------------------------------------------------
da = da.replace('\n',' ')
da = da.replace('<pre>','')
da = da.replace('</pre>','')
da = da.strip()

# Now hunt down the temperature and dewpoint field
# ------------------------------------------------
ray = da.split(' ')
o = None
for el in ray:
	if el[0] == 'T':
		o = el[1:5] # I only want the temperature
if o == None:
	print 'unavailable'
	raise  SystemExit

# First digit after the "T" is a flag to indicate minus (==1)
# -----------------------------------------------------------
if o[0:1] == '1':
		celsius = -(float(o[1:]) / 10.0)
else:
	celsius = float(o[1:]) / 10.0

# And you know, celsius just isn't for people. Farenheit is better. So:
# ---------------------------------------------------------------------
farenheit = celsius * (9.0/5.0) + 32.0
o = "%.1f" % (farenheit)

# And at last, we have the temperature:
print '%sºF' % o

