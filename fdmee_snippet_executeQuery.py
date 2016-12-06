'''
 Snippet:       Loop records in ResultSet object (executeQuery)
 Author:        Francisco Amores
 Date:          12/06/2016
 Blog:          http://fishingwithfdmee.blogspot.com
 
 Notes:         This snippet can be pasted in any event/custom script.
                
                Function executeQuery executes SQL queries in the
                FDMEE database
                
 Instructions:  Set log level (global or application settings) to 5 
 Hints:         Use this snippet to execute a SQL query with API
                function executeQuery and loop all records in the 
                ResultSet object returned by API.
                
                This snippet can be also used with other API functions
                returning ResultSet objects
                
 Example:       Get distinct keys for POV components
               
 FDMEE Version: 11.1.2.3 and later
 ----------------------------------------------------------------------
 Change:
 Author:
 Date:
'''

# Import section
import java.sql.SQLException as SQLException
import os # Optional

# SQL Query (Example -> get distinct partitionkey, catkey, and periodkey for specific load id)
sqlQuery = """
            SELECT                
            DISTINCT PARTITIONKEY,
            CATKEY,
            PERIODKEY
            FROM TDATASEG
            WHERE LOADID = ?"""

# List of parameters
# Emtpy list ([]) if no parameters (?) are required -> params = []
loadId = fdmContext["LOADID"]            
params = [loadId]             

# Debug query
fdmAPI.logDebug("SQL Query (params):%s %s (%s)" % (os.linesep, sqlQuery, params))

try:
    # Execute query (returns ResultSet)
    # You can also use any API function returning a ResultSet
    rs = fdmAPI.executeQuery(sqlQuery, params)
    
    # Loop records if resulset has data
    if rs.isBeforeFirst():
        while rs.next():
            # Get column values
            partKey = rs.getString("PARTITIONKEY")
            catKey = rs.getString("CATKEY")
            periodKey = rs.getString("PERIODKEY")
            
            # Write to log (Optional)
            fdmAPI.logDebug("POV Keys: %s, %s, %s" % (partKey, catKey, periodKey))
            
            # Code executed for each record
            # ...  
    else:
        # No records
        fdmAPI.logDebug("No records returned!")    
    
    # Close ResultSet
    fdmAPI.closeResultSet(rs)
    
except (SQLException, Exception), ex:
    # Error message
    errMsg = "Exception: %s" % ex
    fdmAPI.logFatal(errMsg)
    # Optionally raise RunTimeError to stop the process
    # raise RunTimeError(errMsg)

