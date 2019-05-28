def get_odi_source_details(fdmAPI, fdmContext, sourceSystemName, logicalSchema):
    '''
     Snippet:      Get ODI Source details for Source System Name 
     Author:       Francisco Amores
     Date:         21/05/2019
           
     Parameters:   
                   - fdmAPI: FDMEE API object
                   - fdmContext: FDM Context object
                   - sourceSystemName: Source System name 
                   - logicalSchema: ODI Logical Schema
                   
     Notes:         This snippet can be pasted in any event script
     
     FDMEE Version: 11.1.2.3 and later
               
     ----------------------------------------------------------------------
     Change:
     Author:
     Date:
    '''
    
    # *******************************************
    # Import section
    # *******************************************
    from java.sql import SQLException
    
       
    # *******************************************
    # Get ODI Details for Source System
    # *******************************************
    
    # log
    logMsg = "Getting ODI details for Source System %s" % (sourceSystemName)
    fdmAPI.logInfo(logMsg)
    
    sqlOdiDetails = """SELECT
                        S.SOURCE_SYSTEM_NAME,
                        C.CONTEXT_CODE AS ODI_CONTEXT,
                        CO.CON_NAME AS DATA_SERVER_NAME,
                        L.LSCHEMA_NAME AS LOGICAL_SCHEMA,
                        P.SCHEMA_NAME AS PHYSICAL_SCHEMA,
                        TXT.FULL_TXT AS JAVA_URL,
                        CO.JAVA_DRIVER,
                        CO.USER_NAME,
                        CO.PASS AS ENCRYPTED_PWD
                    FROM 
                        AIF_SOURCE_SYSTEMS S INNER JOIN SNP_CONTEXT C
                            ON S.ODI_CONTEXT_CODE = C.CONTEXT_CODE
                        INNER JOIN SNP_LSCHEMA L
                            ON L.LSCHEMA_NAME = ?
                        INNER JOIN SNP_PSCHEMA_CONT PC
                            ON PC.I_CONTEXT = C.I_CONTEXT AND
                               PC.I_LSCHEMA = L.I_LSCHEMA
                        INNER JOIN SNP_PSCHEMA P
                            ON P.I_PSCHEMA = PC.I_PSCHEMA
                        INNER JOIN SNP_CONNECT CO
                            ON P.I_CONNECT = CO.I_CONNECT
                        INNER JOIN SNP_MTXT TXT
                            ON CO.I_TXT_JAVA_URL = TXT.I_TXT
                        LEFT OUTER JOIN SNP_CONNECT_PROP CP
                            ON CP.I_CONNECT = CO.I_CONNECT
                    WHERE S.SOURCE_SYSTEM_NAME = ?"""
    
    # params
    params = [logicalSchema, sourceSystemName]
    
    try:
        # execute SQL query
        rsOdiDetails = fdmAPI.executeQuery(sqlOdiDetails, params)
        
        # initialize map
        mapOdiDetails = {}
        
        # loop
        if rsOdiDetails.isBeforeFirst():
            while rsOdiDetails.next():
                # get ODI details
                odiContext = rsOdiDetails.getString("ODI_CONTEXT")
                odiDataServer = rsOdiDetails.getString("DATA_SERVER_NAME")
                odiPSchema = rsOdiDetails.getString("PHYSICAL_SCHEMA")
                odiJavaUrl = rsOdiDetails.getString("JAVA_URL")
                odiJavaDriver = rsOdiDetails.getString("JAVA_DRIVER")
                odiUserName = rsOdiDetails.getString("USER_NAME")
                odiPwd = rsOdiDetails.getString("ENCRYPTED_PWD")
                # add to dictionary
                mapOdiDetails["ODI_CONTEXT"] = odiContext
                mapOdiDetails["DATA_SERVER_NAME"] = odiDataServer
                mapOdiDetails["PHYSICAL_SCHEMA"] = odiPSchema
                mapOdiDetails["JAVA_URL"] = odiJavaUrl
                mapOdiDetails["JAVA_DRIVER"] = odiJavaDriver
                mapOdiDetails["USER_NAME"] = odiUserName
                mapOdiDetails["ENCRYPTED_PWD"] = odiPwd
                
                # log
                fdmAPI.logInfo("ODI Details: %s" % mapOdiDetails)
        else:
            # ODI Details not found                        
            errMsg = "ODI Details not found for Source System name %s (Logical Schema %s)" % sourceSystemName, logicalSchema
            fdmAPI.logInfo(errMsg)
            raise RuntimeError(errMsg)        
        # close rs
        fdmAPI.closeResultSet(rsOdiDetails)
    except SQLException, ex:
        errMsg = "Error executing the SQL Statement: %s" % ex
        raise RuntimeError(errMsg)
        
    # return
    return mapOdiDetails