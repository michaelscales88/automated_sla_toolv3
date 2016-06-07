Option Explicit

Const ErrorInvalidArgs = 1
Const ErrorInvalidServerName = 2
Const ErrorInvalidDatabaseName = 3

Const ErrorCreateSQLDMO = 4
Const ErrorConnectToServer = 5
Const ErrorConnectToDatabase = 6

Const ErrorCreateFileSystemObject = 7

Const ErrorDatabaseAlreadyExists = 8
Const ErrorCreateDatabase = 9
Const ErrorOpenProvisioningFile = 10

Const ErrorDatabaseMissing = 11
Const ErrorDeleteDatabase = 12

Const ErrorSQLXMLBulkLoad = 13
Const ErrorImportFailed = 14

Const ErrorNoFileList = 15
Const ErrorExportFailed = 16
Const ErrorEmptyFileList = 17
Const ErrorCreateXMLDOM = 18

Const ErrorSQLSprocFailed = 19

Const ForReading = 1
Const ForWriting = 2

Const FormatDefault = -2
Const FormatUnicode = -1
Const FormatASCII = 0

Dim g_fso
Dim g_xmldoc

' Create a global instance of the FileSystemObject
On Error Resume Next
Set g_fso = CreateObject("Scripting.FileSystemObject")
If (Err.Number <> 0 or g_fso Is Nothing) Then
	WScript.Echo "Microsoft VBScript runtime is not present or properly installed."
	WScript.Quit ErrorCreateFileSystemObject
End If
On Error Goto 0

Set g_xmldoc = CreateObject("MSXML2.DOMDocument.3.0")
If (Err.Number <> 0 or g_xmldoc Is Nothing) Then
	Set g_xmldoc = Nothing
End If

'----------------------------------------------------------------------
' Make sure the imported XML is valid. Returns True if the xml is valid.
'----------------------------------------------------------------------
Function ValidateXML(strXMLFilePath)
    ValidateXML = False
    
    g_xmldoc.load(strXMLFilePath)
    If (g_xmldoc.parseError.errorCode = 0) Then 
        ValidateXML = True
    End If
End Function

'----------------------------------------------------------------------
' See if SQLXML is installed.
'----------------------------------------------------------------------
Sub TestSQLXML()
    Dim sqlbl

    On Error Resume Next
    Set sqlbl = CreateObject("SQLXMLBulkLoad.SQLXMLBulkLoad")
    If (Err.Number <> 0 Or sqlbl Is Nothing) Then
	    WScript.Echo "The SQLXML component must be installed on this computer in order to perform the import operation. Please see the OMPM documentation for instructions how to install SQLXML."
	    Set sqlbl = Nothing
	    On Error Goto 0
	    WScript.Quit ErrorSQLXMLBulkLoad
	Else
	    Set sqlbl = Nothing
	    On Error Goto 0
	    WScript.Quit 0   
    End If
End Sub

'----------------------------------------------------------------------
' Tests a connection to a SQL Database.
'----------------------------------------------------------------------
Sub TestSQLConnect(strServer, strDatabase)
    Dim objSQLServer
    Dim objDatabase
    
    'If any of these fail, they will exit with a non-zero value
    GetSQLServer objSQLServer 
    Connect objSQLServer, strServer
    GetDatabase objSQLServer, objDatabase, strDatabase
    
    'Success, exit with zero
    WScript.Quit 0
End Sub

'----------------------------------------------------------------------
' See if Server Name is valid.
'----------------------------------------------------------------------
Sub CheckServerName(strServerName)
    If (Len(strServerName) = 0) Then
	    WScript.Echo "ERROR: Invalid server name."
	    WScript.Quit ErrorInvalidServerName
    End If
End Sub
    
'----------------------------------------------------------------------
' See if Database Name is valid.
'----------------------------------------------------------------------
Sub CheckDatabaseName(strDatabaseName)
    If (Len(strDatabaseName) = 0 Or Len(strDatabaseName) > 123) Then
        WScript.Echo "ERROR: Invalid database name."
        WScript.Quit ErrorInvalidDatabaseName
    End If
End Sub

'----------------------------------------------------------------------
' Ensure that SQLDMO is installed.
'----------------------------------------------------------------------
Sub GetSQLServer(objSQLServer)
    set objSQLServer = Nothing
    On Error Resume Next
    Set objSQLServer = CreateObject("SQLDMO.SQLServer")
    If (Err.Number <> 0) Then
	    WScript.Echo "SQL-DMO Install Required: This operation requires the SQL Server ODBC Driver, version 3.80 or later, which comes with SQL Server 2000, SQL Server 2005 and SQL Server Express."
	    WScript.Echo ""
	    WScript.Echo "Please See the OMPM documentation for more information:"
	    WScript.Echo "http://technet2.microsoft.com/Office/f/?en-us/library/27ffcab8-40f1-4687-808d-6d79fb8536bd1033.mspx"
	    WScript.Quit ErrorCreateSQLDMO
    End If
    On Error Goto 0
End Sub
    
'----------------------------------------------------------------------
' Connect to the server.
'----------------------------------------------------------------------
Sub Connect(objSQLServer, strServerName)
    objSQLServer.LoginTimeout = 30
    objSQLServer.QueryTimeout = 3600
    objSQLServer.LoginSecure = True
    On Error Resume Next
    objSQLServer.Connect strServerName
    If (Err.Number <> 0) Then
	    WScript.Echo "ERROR: Cannot connect to server: " & strServerName
	    If (Len(Trim(Err.Description)) > 0) Then
		    WScript.Echo Err.Description
	    End If
	    WScript.Quit ErrorConnectToServer
    End If
    On Error Goto 0
End Sub
    
'----------------------------------------------------------------------
' Get a database object from the server.
'----------------------------------------------------------------------
Sub GetDatabase(objSQLServer, objDatabase, strDatabaseName)
    set objDatabase = Nothing
    On Error Resume Next
    set objDatabase = objSQLServer.Databases(strDatabaseName)
    If (Err.Number <> 0) Then
	    WScript.Echo "ERROR: Cannot connect to database: " & strDatabaseName
	    If (Len(Trim(Err.Description)) > 0) Then
		    WScript.Echo Err.Description
	    End If
	    WScript.Quit ErrorConnectToDatabase
	End If
    On Error Goto 0
End Sub

'----------------------------------------------------------------------
' Main entry point.
'   USAGE: Common arg
'
' Arguments:
'   testsqlxml - checks that SQLXML is installed. Quits with a positive 
'                error code if SQLXML is not installed.
'   testsqlconnect - attempts to connect to a SQL database. Quits with a 
'                    positive error code if the connection fails.
'   validatexml - loads xml file into a xmldoc object to check if it is 
'                 valid.
'-----------------------------------------------------------------------
Dim args

Set args = WScript.Arguments

If (args.Count >= 1) Then
    If (args(0) = "testsqlxml") Then
        TestSQLXML
    ElseIf (args(0) = "testsqlconnect") Then
        If(args.Count = 3) Then
            TestSQLConnect args(1), args(2)
        Else
            WScript.Echo "ERROR: Invalid testsqlconnect args."
            WScript.Echo "Usage: Common.vbs testsqlconnect <ServerName> <DatabaseName>"
            WScript.Quit ErrorInvalidArgs
        End If
    ElseIf (args(0) = "validatexml") Then
        If (args.Count <> 2) Then
            WScript.Echo "ERROR: Invalid validatexml args."
            WScript.Echo "Usage: Common.vbs validatexml <XmlFile>"
            WScript.Quit ErrorInvalidArgs
        End If
        If (ValidateXML(args(1))) Then
            WScript.Echo "Xml is valid."
        Else
            WScript.Echo "Xml is invalid."
        End If
    ElseIf (args(0) = "sleep") Then
        WScript.Sleep CInt(args(1))*1000
    End If
End If