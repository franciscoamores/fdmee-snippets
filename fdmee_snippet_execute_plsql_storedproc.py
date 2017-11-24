'''
 Snippet:       Execute a PL/SQL stored procedures IN/OUT params
 Author:        Francisco Amores
 Date:          24/11/2017
 Blog:          http://fishingwithfdmee.blogspot.com
 
 Notes:         This snippet can be pasted in any event script.
                Content of fdmContext object will be logged in the
                FDMEE process log (...\outbox\logs\)
                
                This snippet executes the stored procedure via dblink
                Local stored procedures are executed in a similar way
                
 Instructions:  Set log level (global or application settings) to > 4 
 Hints:         You can implement also code to get db connection details
                instead of hard-coding
               
 FDMEE Version: 11.1.2.3 and later
 ----------------------------------------------------------------------
 Change:
 Author:
 Date:
'''
try:
    # Import Java libraries
    import java.sql.SQLException as SQLException
    import java.sql.DriverManager as SQLDriverMgr
    import java.sql.CallableStatement as SQLCallableStmt
    import java.sql.Types as SQLTypes
    import java.sql.Date as SQLDate # needed for DATE parameters
    import java.text.SimpleDateFormat as SimpleDateFormat
    
    # Note: import any other class you need
    
except ImportError, err:
    errMsg = "Error importing libraries: %s" % err
    fdmAPI.logFatal(errMsg)
    raise RuntimeError(errMsg)

# ----------------------------------------
# Connect to FDMEE or External database
# ----------------------------------------

# Connection details
dbConn = "the jdbc url"
dbUser = "the db user"
dbPasswd = "the db password"

try:        
    # get connection to database for callable statements        
    conn = SQLDriverMgr.getConnection(dbConn, dbUser, dbPasswd)
    fdmAPI.logInfo("Connected to the database")
except SQLException, ex:
    errMsg = "Error executing SQL: %s" % (ex)
    raise RuntimeError("Error generated from FDMEE script\n%s" % errMsg)

# ----------------------------------------
# Execute PL/SQL Stored Procedure
# ----------------------------------------

# Get dblink
dbLink = "your dblink"

# PL/SQL Block Code (via DBLINK)
'''
    Procedure implemeted as:
    PROCEDURE CARGA_TABLA(P1            OUT VARCHAR2,
                          P2            OUT NUMBER,
                          P3            IN NUMBER,
                          P4            IN DATETIME,
                          P5            IN VARCHAR2,
                          P6            IN VARCHAR2,
                          P7            IN VARCHAR2,
                          P8            IN VARCHAR2,                          
                          P9            IN VARCHAR2)
'''

# Each ? represents one stored proc parameter
# Ex: schema.package.storedproc if your stored proc is in a package
plSqlBlock = "{CALL schema.package.storedproc@%s(?, ?, ?, ?, ?, ?, ?, ?, ?)}" % dbLink

# Get parameters for the statement
p3 = "valuep3"
# parameter p4 must be passed as java.sql.Date
sdf = SimpleDateFormat("dd/MM/yyyy")
dtParsed = sdf.parse("date value")
p4 = SQLDate(dtParsed.getTime())
p5 = "this param is passed as null"
p6 = "valuep6"
p7 = "valuep7"
p8 = "valuep8"
p9 = "valuep9"

# Prepare and execute call
try:
    # Callable Statement    
    callableStmt = conn.prepareCall(plSqlBlock)
    fdmAPI.logInfo("Callable statement successfully prepared")
    
    # Set IN parameters
    callableStmt.setBigDecimal("p3", p3)    
    callableStmt.setDate("p4", p4)
    callableStmt.setNull("p5", SQLTypes.VARCHAR) # NULL
    callableStmt.setString("p6", p6)
    callableStmt.setString("p7", p7)
    callableStmt.setString("p8", p7)
    callableStmt.setString("p9", p7)      
    fdmAPI.logInfo("Parameters IN set")
    
    # Register OUT parameters
    callableStmt.registerOutParameter("p1", SQLTypes.VARCHAR)    
    callableStmt.registerOutParameter("p2", SQLTypes.NUMERIC)
    fdmAPI.logInfo("Parameters OUT registered")
        
    # Execute PL/SQL Stored Procedure
    result = callableStmt.execute()
    conn.commit()
    fdmAPI.logInfo("Stored Proceedure successfully executed: %s" % result)
    
    # Get OUT parameters
    p1 = callableStmt.getString("p1")
    p2 = callableStmt.getInt("p2")

    # Log OUT parameters
    fdmAPI.logInfo("OUT p1:  %s" % p1)
    fdmAPI.logInfo("OUT p2:  %s" % p2)
    
except (Exception, SQLException), ex:
    errMsg = "Error when executing the stored procedure: %s" % ex
    fdmAPI.logFatal(errMsg)
    if len(errMsg) <= 1000:
        fdmAPI.showCustomMessage(errMsg)
    raise RuntimeError(errMsg)

# ----------------------------------------
# Close connection
# ----------------------------------------
if callableStmt is not None:
    callableStmt.close()
if conn is not None:
    conn.close()
    fdmAPI.logInfo("DB connection closed")
