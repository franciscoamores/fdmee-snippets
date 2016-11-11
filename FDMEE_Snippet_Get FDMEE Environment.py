'''
 Snippet:       Get environment running the script based on the FDMEE Server
                hostname
 Author:        Francisco Amores
 Date:          11/11/2016
 Blog:          http://fishingwithfdmee.blogspot.com
 
 Notes:         This snippet can be pasted in any event/custom/import script.
                Output will be logged in the FDMEE process log 
                (...\outbox\logs\)
                
                This script uses socket python module
                
 Instructions:  Set log level (global or application settings) to 5 
                To add new servers, include an entry in the dictionary.
                You can get hostnames by executing command "hostname"
                from the command line in the FDMEE server(s).
 
 Hints:         Use this snippet to avoid having different script codes
                across environments. The right code will be executed
                at runtime based on the FDMEE server running the process
               
 FDMEE Version: 11.1.2.3 and later
 ----------------------------------------------------------------------
 Change:
 Author:
 Date:
'''

# import socket module
import socket

# Dictionaty for FDMEE Servers
# These are sample servers and should be replaced by existing ones
dictFDMEEServers = { 
                     "FDMEE_SERVER_DEV" : "DEV",
                     "FDMEE_SERVER_PROD1": "PROD",
                     "FDMEE_SERVER_PROD2": "PROD"
                   }

# get hostname
hostName = socket.gethostname()

# Assign envFDMEE based on FDMEE Server
try:
    envFDMEE = dictFDMEEServers[hostName]
except KeyError, err:
    errMsg = "FDMEE Server does %s not exist inthe dictionary dictFDMEEServers" % hostName
    fdmAPI.showCustomMessage(errMsg)
    raise RuntimeError(errMsg)
    
# Debug
fdmAPI.logDebug("FDMEE Server: %s (%s)" % (hostName, envFDMEE))

# ****************************************************************
# Specific Code for Development
# ****************************************************************
if envFDMEE == "DEV":
    # Debug
    fdmAPI.logDebug("Code for %s" % envFDMEE)
    
    # your code here

# ****************************************************************
# Specific Code for Production
# ****************************************************************
if envFDMEE == "PROD":
    # Debug
    fdmAPI.logDebug("Code for %s" % envFDMEE)
    
    # your code here 

# ****************************************************************
# Specific Code for Environment XXX
# ****************************************************************
if envFDMEE == "XXX":
    # Debug
    fdmAPI.logDebug("Code for %s" % envFDMEE)
    
    # your code here  


# ****************************************************************
# Code for all environments
# ****************************************************************

# your code here
