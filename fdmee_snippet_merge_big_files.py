'''
 Snippet:       Merge a list of files
 Author:        Francisco Amores
 Date:          11/11/2016
 Blog:          http://fishingwithfdmee.blogspot.com
 
 Notes:         This snippet can be pasted in any event script.
                Content of fdmContext object will be logged in the
                FDMEE process log (...\outbox\logs\)
                
 Instructions:  Set log level (global or application settings) to > 4 
 Hints:         Use this snippet to merge multiple single files into
                ont.
                It copies files in chunks to avoid memory issues
               
 FDMEE Version: 11.1.2.3 and later
 ----------------------------------------------------------------------
 Change:
 Author:
 Date:
'''

# initialize
srcFolder = r"C:\temp"
tgtFolder = r"C:\temp"
listSrcFilename = ["file1.txt", "file2.txt", "file3.txt"]
tgtFilename = "merge.txt"

# import section
import os
import shutil

try:
    # Open Target File in write mode
    tgtFilepath = os.path.join(tgtFolder, tgtFilename)
    tgtFile = open(tgtFilepath, "w")
    # Log
    fdmAPI.logInfo("File created: %s" % tgtFilepath)    
    
    # Loop source files to merge
    for srcFilename in listSrcFilename:
    
        # file path
        filepath = os.path.join(srcFolder, srcFilename)          
        # Log
        fdmAPI.logInfo("Merging file: %s" % filepath)                    
        # Open file in read mode
        srcFile = open(filepath, "r")        
        # Copy source file into target
        # 10 MB per writing chunk to avoid big file into memory
        shutil.copyfileobj(srcFile, tgtFile, 1024*1024*10)
        # Add new line char in the target file
        # to avoid issues if source file don't have end of line chars
        tgtFile.write(os.linesep)
        # Close source file
        srcFile.close()
        # Debug
        fdmAPI.logInfo("File merged: %s" % file)
        
    # Close target file
    tgtFile.close()
                    
except (IOError, OSError), err:
    raise RuntimeError("Error concatenating source files: %s", err)