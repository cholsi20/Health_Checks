#!/usr/bin/python

#
# Created by Courtney Holsinger
# June 30, 2016
# Health Check Program 1 - Customer File Drop Confirmation on Exattarget FTP Server
#
# The intent of this program is to check whether or not the customer file has dropped at the alotted time.
# Failure to locate the file at specified times should return a 2 (CRITICAL), and trigger a PagerDuty Alert.
# Success should return a 0 (OKAY) and trigger no alert or email.

#--- BEGIN PROGRAM ---#
#--------------------------------------------------------------- IMPORT CALLS -----
import paramiko #SSH/ SFTP module
import sys #returns those handy dandy exit codes for Icinga

import os.path #potentially not important 
from datetime import datetime #you need to do this to call the now() method - i.e. you cannot just import datetime

#---------------------------------------------------------- VARIABLE INITILIZATION -----
date = datetime.now()
yearString = '{}'.format( date.year ) #formats year as a string

#logic to format month to match file formatting
monthInt = date.month
#if the month is less than ten, format appropriately
if date.month < 10:
   monthInt = format( date.month, "02d")

monthString='{}'.format( monthInt )
#print( monthString )

#logic to format day to match file formatting
dayInt = date.day
#if the day is less than 10, format appropriately
if date.day < 10:
   dayInt = format( date.day, "02d")

dayString = '{}'.format( dayInt )
#print( dayString )

#logic to determine AM vs. PM
hourString = "" #because hopefully you can modify empty strings in Python
if date.hour < 12:
   hourString = "AM"
else:
   hourString = "PM"

#------------------------------------------------------------------------- Begin File Checks -----------------------
# Connect to the Exacttarget FTP Server... 
# Stangely, a more challenging prospect than one would initially imagine
try:
   # Establish login credential variables using SFTP
   host = "ftp.s4.exacttarget.com" #used to SFTP into a remote server - gives you access to walk remote file system
   port = 22
   transport = paramiko.Transport ((host, port))

   #authorize
   transport.connect(username = '1047431', password = 'A.x6fD7.F.') #connects you to the server using server credentials

   #sftp into the server
   sftp = paramiko.SFTPClient.from_transport(transport)

   #customerFile = sftp.stat("import2016_07_07_AM_sales_COPY.tsv") #Retrieve information about the file on the remote system - returns an SFTPAttributes Object containing attributes about the file
   filesList = sftp.listdir("/import/dailyEmailFilesPROD/")

   # This would print all the files and directories
   for file in filesList:
     if file.__eq__(yearString + "_" + monthString + "_" + dayString + "_" + hourString + "_customers.tsv.gz"):     
       print( "true" )
       sys.exit( 0 )
       
     else:
       print( "false" )
       sys.exit( 2 )

# If unable to connect to server
except IOError:
  # Return error message of "Unable to connect to FTP server - server may be down"
  # Prompts PagerDuty Alert with a Warning
  sys.exit( 1 )

finally:
  #disconnect from the server
  print ("finally")
