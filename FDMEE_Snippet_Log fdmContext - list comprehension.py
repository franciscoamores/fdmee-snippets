'''
 Snippet:       Log content of fdmContext object
 Author:        Francisco Amores
 Date:          11/11/2016
 Blog:          http://fishingwithfdmee.blogspot.com
 
 Notes:         This snippet can be pasted in any event script.
                Content of fdmContext object will be logged in the
                FDMEE process log (...\outbox\logs\)
                
                This script uses list comprehension builder
                
 Instructions:  Set log level (global or application settings) to 5 
 Hints:         Use this snippet to see different context values
                at any workflow step.
               
 FDMEE Version: 11.1.2.3 and later
 ----------------------------------------------------------------------
 Change:
 Author:
 Date:
'''

# initialize 
logLines = ""

# List comprehension
# Define list with pairs "Key: Value" from sorted fdmContext
list = ["%s: %s" % (key, fdmContext[key]) for key in sorted(fdmContext)]
# List is then joined with "\n" character (newline)
logLines = "\n".join(list)
   
# write line to log (Debug)
if logLines:
    fdmAPI.logDebug("Content of fdmContext: \n%s" % logLines)
else:
    fdmAPI.logWarn("Nothing to log from fdmContext")
