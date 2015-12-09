#!/usr/bin/python
# -*- coding: utf-8 -*-

# Two defaults I suggest you set up:
# ----------------------------------

# (1) Construct default stationid (see "Configuration" in README.md)
# You can override this with -s or --station. i.e. "./tmp.py -s lax"
# ----------------------=========-----------------------------------
stationid	= "xxxMTRggw"	# Glasgow, MT - this works
#stationid	= "xxxMTRanc"	# Anchorage, AK - this does NOT work
#stationid	= "xxxMTRlax"	# Los Angeles, CA - this works
#stationid	= "xxxMTRjfk"	# JFK airport, NYC, NY - this works
#stationid	= "xxxMTRmia"	# Miami, FL - this works

# (2) Set mode for the temperature scale you prefer (F is best for humans):
# You can override this with -m/--mode N, -c/--celsius, -k/--kelvin, etc.
# --------====-------------------------------------------------------------
# mode:
#       0 Celsius
#       1 Fahrenheit
#       2 Kelvin
#       3 Rankine
#       4 Réaumur
# ------------------
mode = 1 # This is the default mode you prefer.

# CODE below this line you probably don't need to worry about
# -----------------------------------------------------------

#     Project: tmp.py
#      Author: fyngyrz  (Ben)
#     Contact: fyngyrz@gmail.com (bugs, feature requests, kudos, bitter rejections)
#     Project: tmp.py
#    Homepage: https://github.com/fyngyrz/NWS-Temperature
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
#     LastRev: December 26th, 2015
#  LastDocRev: December 26th, 2015
# Tab spacing: 4 (set your editor to this for sane formatting while reading)
#Dev/Test Env: Ubuntu 12.04.5 LTS, Python 2.7.3, Raspbian 7.6
#  Also works: OS X 10.6.8, Python 2.6.1
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
# ------------------------------------------------------------------------------
#     Version: 0.5
#     Changes:
#         0.5:	++tests for wget and reports if missing, autocofigs it
#         0.4:	++command line option for station ID
#         0.3:	++command line options, some error checking
#         0.2:	No longer uses tmp file. Pipes wget into Python instead.
#				Checks Python version and adjusts pipe mechanism
#		  0.0:	(Unversioned) Original Release

# Here's what is in the typical NWS METAR data chunk we're fetching:
# ==================================================================
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

import sys
import subprocess

version = sys.version_info
if version[0] != 2:
	print 'Requires Python 2'
	exit()
if version[1] < 4:
	print 'Requires higher than Python 2.3'
	exit()

# Locate wget command
# -------------------
cmdlist = ['which','wget']
if version[1] < 7:
	cmdstr = ' '.join(cmdlist)
	p = subprocess.Popen(cmdstr,stdout=subprocess.PIPE,shell=True)
	wgetloc,err = p.communicate()
else:
	wgetloc = subprocess.check_output(cmdlist)
wgetloc = wgetloc.strip()

if wgetloc == '':
	print "The wget command doesn't seem to be installed. It's required."
	exit()

omode = mode
	
mnames = ['centigrade','fahrenheit','kelvin','rankine','reaumur']
def help():
	global omode,mnames
	print 'Without parameters, uses default mode of %s' % (mnames[omode])
	print '-s or --station  [3-letter station ID, ie ggw]'
	print '-h or --help or ?'
	print '-m or --mode [int] (int 0-4 = c,f,k,ra,re)'
	print '-c or --centigrade'
	print '-k or --kelvin'
	print '-f or --fahrenheit'
	print '-ra or --rankine'
	print '-re or --reaumur'

if omode < 0 or omode > 4:
	print 'ERROR: invalid default mode: Must be 0...4'
	exit()

mflag = False
sflag = False
if len(sys.argv) > 1:
	for arg in sys.argv[1:]:
		if arg == '-m' or arg == '--mode':
			mflag = True
		elif arg == '?' or arg == '-h' or arg == '--help':
			help()
			exit()
		elif arg == '-s' or arg == '--station':
			sflag = True
		elif arg == '-c' or arg == '--centigrade': # c f k ra re
			mode = 0
		elif arg == '-f' or arg == '--fahrenheit': # c f k ra re
			mode = 1
		elif arg == '-k' or arg == '--kelvin': # c f k ra re
			mode = 2
		elif arg == '-ra' or arg == '--rankine': # c f k ra re
			mode = 3
		elif arg == '-re' or arg == '--reaumur': # c f k ra re
			mode = 4
		elif sflag == True:
			if len(arg) != 3:
				print '-s/--station requires a 3-letter station ID'
				exit()
			stationid = 'xxxMTR%s' % (arg.lower())
		elif mflag == True:
			mflag = False
			try:
				mode = int(arg)
				if mode < 0 or mode > 4:
					raise
			except:
				print '-m / --mode option requires an integer [0-4]'
				exit()
		else:
			help()
			exit()

# --------------------------------------------------------------------
# The piping was extremely finicky to get going. Under Python 2.6, the
# tx parameter has to be enclosed in double quotes. Under 2.7, it cannot
# be so enclosed. 2.7 takes a sequence as documented; but 2.6 would not
# take a sequence, and required a string, which is *not* what the
# Python documentation for 2.6 says. I've got this switching how it
# works based on Python 2.7 and above, or lesser; but I've little
# confidence that it will actually perform on anything but the two
# versions I've actually tested it on. Any further versioning you do
# will be of interest to me (other than Python 3, of course. That's no
# more Python than a Chicago deep-dish cassarole is a proper pizza.)
# --------------------------------------------------------------------

# Go get the NWS data:
# --------------------
if version[1] < 7:
	tx = '"http://www.wrh.noaa.gov/total_forecast/getprod.php?toggle=textonly&afos=%s"' % (stationid)
	cmdlist = ['%s' % wgetloc,'-q','-O','-',tx]
	cmdstr = ' '.join(cmdlist)
	p = subprocess.Popen(cmdstr,stdout=subprocess.PIPE,shell=True)
	da,err = p.communicate()
else:
	tx = 'http://www.wrh.noaa.gov/total_forecast/getprod.php?toggle=textonly&afos=%s' % (stationid)
	cmdlist = ['%s' % wgetloc,'-q','-O','-',tx]
	da = subprocess.check_output(cmdlist)

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
	if len(el) > 0:
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
if mode == 0: # C
	o = "%.1fºC" % (celsius)
elif mode == 1: # F 
	farenheit = celsius * (9.0/5.0) + 32.0
	o = "%.1fºF" % (farenheit)
elif mode == 2: # K
	kelvin = celsius + 273.15
	o = "%.1fºK" % (kelvin)
elif mode == 3: # Rankine 
	rankine = celsius * 1.8 + 32 + 459.67
	o = "%.1fºRa" % (rankine)
elif mode == 4: # Reamur
	reamur = celsius * 0.08
	o = "%.1fºRe" % (reamur)
else:
	o = 'Unknown mode: "%d"' % (mode)

# And at last, we have the temperature:
print o

