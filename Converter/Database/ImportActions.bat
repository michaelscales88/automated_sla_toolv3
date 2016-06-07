@echo off
if /i '%1'=='-q' shift& goto LParseArgs
if /i '%1'=='/q' shift& goto LParseArgs
@echo.
@echo Microsoft Office Migration Planning Manager version 1.0
@echo Batch Action Import Tool
@echo Copyright (c) 2006 Microsoft Corporation.  All Rights Reserved.
@echo.

:LParseArgs
if '%1'=='-?' goto LUsage
if '%1'=='/?' goto LUsage
if /i '%1'=='help' goto LUsage
if /i '%1'=='-help' goto LUsage
if /i '%1'=='/help' goto LUsage

REM Make sure SQLXML is installed
cscript.exe /NoLogo .\Include\Common.vbs testsqlxml
if not '%ERRORLEVEL%'=='0' goto LError

REM Make sure some arguments were provided.
if '%1'=='' goto LInvalidArg

if /i '%1'=='-s' shift& goto LImportSingleFile
if /i '%1'=='/s' shift& goto LImportSingleFile


REM ----------------------------------------------------------------------
REM Batch Importing
REM ----------------------------------------------------------------------
:LImportBatch
if '%1'=='' goto LInvalidArg
if '%2'=='' goto LInvalidArg
if '%3'=='' goto LInvalidArg
if not '%4'=='' goto LInvalidArg
set SERVER=%1
set DATABASE=%2
set LOGDIR=%3
set FILESPROCESSED=0

REM Make sure the SQL database is accessible
cscript.exe /NoLogo .\Include\Common.vbs testsqlconnect %SERVER% %DATABASE% 
if not '%ERRORLEVEL%'=='0' goto LError

if not exist %LOGDIR% goto LInvalidArg

@echo Importing Data
@echo.
@echo Do not interrupt this process or launch another import process.
@echo Importing data may take several minutes depending on the amount of data extracted.
@echo.

cscript.exe /NoLogo .\Include\Import.wsf %SERVER% %DATABASE% .\Schemas\ToolDefinitionMapping.xml ".\Tools" -tools

for /d %%d in (%LOGDIR%\*) do (
	for /d %%u in ("%%d"\*) do ((
		for %%f in ("%%u"\Action_*.xml) do call ImportActions.bat -q -s %SERVER% %DATABASE% %LOGDIR% "%%~nxd" "%%~nxu" "%%f")&(
		for %%f in ("%%u"\Action_*.cab) do call ImportActions.bat -q -s -x %SERVER% %DATABASE% %LOGDIR% "%%~nxd" "%%~nxu" "%%f")
	)
)

for /d %%d in (%LOGDIR%\*) do (
	for /d %%u in ("%%d"\*) do (
		call :DeleteFolderIfEmpty "%%u"
	)
)& call :DeleteFolderIfEmpty "%%d"
		
if '%FILESPROCESSED%' == '0' goto LNoActionXML
cscript.exe /NoLogo .\Include\Import.wsf %SERVER% %DATABASE% -postactions
@echo Import operation complete.
goto LOperationComplete

:DeleteFolderIfEmpty
setlocal
set arg1=%1
set FOLDEREMPTY=1
for /d %%f in (%arg1%\*) do set FOLDEREMPTY=0
for %%f in (%arg1%\*) do set FOLDEREMPTY=0
if '%FOLDEREMPTY%'=='1' (
	call :LSubRemoveDir %arg%
)
endlocal& goto LDone

:LNoActionXML
@echo No Companion Tool Action XML was found to import. 
@echo.
@echo Action XML must exist in the ^<PathToLogFile^> folder and Action
@echo XML file names must begin with "Action_".
goto LOperationComplete


REM ----------------------------------------------------------------------
REM Single File (i.e. non-batch) Importing
REM ----------------------------------------------------------------------
:LImportSingleFile
set FILESPROCESSED=1
set EXTRACT=0
if /i '%1'=='-x' shift& set EXTRACT=1
if /i '%1'=='/x' shift& set EXTRACT=1

if '%1'=='' goto LInvalidArg
if '%2'=='' goto LInvalidArg
if '%3'=='' goto LInvalidArg
if '%4'=='' goto LInvalidArg
if '%5'=='' goto LInvalidArg
if '%6'=='' goto LInvalidArg
if not '%7'=='' goto LInvalidArg

set SERVER=%1
set DATABASE=%2
set LOGDIR=%~f3
set LOGDOMAIN=%~4
set LOGCOMPUTER=%~5
set LOGFILE="%~f6"
set IMPORTEDDIR="%LOGDIR%\OMPMImported\%LOGDOMAIN%\%LOGCOMPUTER%"
if not exist %IMPORTEDDIR% mkdir %IMPORTEDDIR%
if not exist %IMPORTEDDIR% @echo ERROR: Cannot create %IMPORTEDDIR%. & goto LError

if '%EXTRACT%'=='1' goto LExtractAndImport

:LImport
@echo Importing file %LOGFILE%...
cscript.exe /NoLogo .\Include\Import.wsf %SERVER% %DATABASE% .\Schemas\ToolExportMapping.xml %LOGFILE% -actions
if not '%ERRORLEVEL%'=='0' goto LError
move %LOGFILE% %IMPORTEDDIR% 1>nul
goto LOperationComplete

:LExtractAndImport
set FILESPROCESSED=1
set EXTRACTDIRROOT=%LOGDIR%\OMPMExtracted
set EXTRACTDIR="%EXTRACTDIRROOT%\%LOGDOMAIN%\%LOGCOMPUTER%"
rd /q /s %EXTRACTDIR% 2>nul
if EXIST %EXTRACTDIR% (
@echo File %LOGFILE% failed to import because folder %EXTRACTDIR% could not be removed. 
@echo Please manually remove this folder before attempting to import again.
goto LError
)
if not exist %EXTRACTDIR% mkdir %EXTRACTDIR%
if not exist %EXTRACTDIR% @echo ERROR: Cannot create %EXTRACTDIR%. & goto LError

:LExpand
@echo Extracting files from %LOGFILE%...
call :LExpandWrapper %EXTRACTDIR%
if not '%ERRORLEVEL%'=='0' (
	call :LSubRemoveDir %EXTRACTDIRROOT% 
	goto LExpandError
)
@echo Importing extracted data...
cscript.exe /NoLogo .\Include\Import.wsf %SERVER% %DATABASE% .\Schemas\ToolExportMapping.xml %EXTRACTDIR% -actions -bulk
if not '%ERRORLEVEL%'=='0' (
	call :LSubRemoveDir %EXTRACTDIRROOT%
	goto LError
)
move %LOGFILE% %IMPORTEDDIR% 1>nul
call :LSubRemoveDir %EXTRACTDIRROOT%

goto LOperationComplete


:LOperationComplete
@echo.
goto LDone

:LExpandWrapper
expand.exe %LOGFILE% -F:* "%~f1" 1>nul
goto LDone

:LExpandError
@echo ERROR: Failed to extract files from %LOGFILE%.
goto LError


REM----------------------------------------------------
REM Subroutine for removing directory 
REM Attempts multiple times with exponential backoff
REM----------------------------------------------------
:LSubRemoveDir
if '%1'=='' goto LDone
setlocal
set REMDIR=%1
set TimeoutSeconds=0
set MaxTime=50
:LRetryAttempt
IF EXIST %REMDIR% (
 rd /q /s %REMDIR% 2>nul
)ELSE (
 goto LExitRetryAttempt
)
cscript.exe /NoLogo .\Include\Common.vbs sleep %TimeoutSeconds%
set /A TimeoutSeconds=%TimeoutSeconds%*2+1
if %TimeoutSeconds% LSS %MaxTime% goto LRetryAttempt

@echo The temporary folder %REMDIR% could not be removed. This will be attempted again on the next import.
Set TimeoutSeconds=
Set MaxTime=
endlocal
goto LError

:LExitRetryAttempt
Set TimeoutSeconds=
Set MaxAttempt=
endlocal
goto LDone


:LError
@echo.
goto LDone

:LInvalidArg
@echo ERROR: Invalid parameter usage.
@echo.

:LUsage
@echo USAGE:    ImportActions.bat ServerName DatabaseName PathToLogFile
@echo.
@echo EXAMPLE:  ImportActions.bat SQL001 OMPM c:\logfiles
@echo.
@echo ^<PathToLogFile^> is the root folder containing log file directories 
@echo for domain name and computer name. You must have read/write/create 
@echo permissions for the folder.
@echo.
@echo Please see the Microsoft Office Migration 
@echo Planning Manager documentation for further
@echo information.
@echo.

:LDone
