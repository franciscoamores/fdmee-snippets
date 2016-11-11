'''
 Snippet:       Log content of fdmContext object
 Author:        Francisco Amores
 Date:          11/11/2016
 Blog:          http://fishingwithfdmee.blogspot.com
 
 Notes:         This snippet can be pasted in any event script.
                Content of fdmContext object will be logged in the
                FDMEE process log (...\outbox\logs\)
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

# loop all fdmContext keys (sorted)
for key in sorted(fdmContext):
    # get key value
    value = fdmContext[key]
    # build log line (property name: property value)
    logLines += "%s: %s\n" % (key, value)

# write line to log (Debug)
if logLines:
    fdmAPI.logDebug("Content of fdmContext: \n%s" % logLines)
else:
    fdmAPI.logWarn("Nothing to log from fdmContext")
