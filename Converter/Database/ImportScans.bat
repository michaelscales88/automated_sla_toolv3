@echo off

if /i '%1'=='-q' shift& goto LParseArgs
if /i '%1'=='/q' shift& goto LParseArgs
@echo.
@echo Microsoft Office Migration Planning Manager version 1.0
@echo Batch Scan Import Tool
@echo Copyright (c) 2006 Microsoft Corporation.  All Rights Reserved.
@echo.

:LParseArgs
if '%1'=='-?' goto LUsage
if '%1'=='/?' goto LUsage
if /i '%1'=='help' goto LUsage
if /i '%1'=='-help' goto LUsage
if /i '%1'=='/help' goto LUsage

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

REM Make sure SQLXML is installed
cscript.exe /NoLogo .\Include\Common.vbs testsqlxml
if not '%ERRORLEVEL%'=='0' goto LError

REM Make sure the SQL database is accessible
cscript.exe /NoLogo .\Include\Common.vbs testsqlconnect %SERVER% %DATABASE% 
if not '%ERRORLEVEL%'=='0' goto LError

if not exist %LOGDIR% goto LInvalidArg

REM Check whether another import process is in progress at this time
osql.exe -S %SERVER% -d %DATABASE% -n -h-1 -E -Q"EXIT(Select ImportInProgress from Process_Control)" > nul

IF %ERRORLEVEL% EQU 1 goto InProgress
IF %ERRORLEVEL% EQU 0 (
	goto okay
) ELSE (
	@echo Failed to retrieve the ImportInProgress bit value
	goto OSQLError
)


:okay
osql.exe -S %SERVER% -d %DATABASE% -n -h-1 -b -E -Q "Update Process_Control Set ImportInProgress = 1, TimeStarted = getdate(), ComputerName = host_name()" > nul
IF %ERRORLEVEL% NEQ 0 (
	@echo Failed to set the ImportInProgress bit to 1
	goto OSQLError
)

@echo Importing Data
@echo.
@echo Do not interrupt this process or launch another import process.
@echo Importing data may take several minutes depending on the amount of data extracted.
@echo.

for %%f in (%LOGDIR%\Scan_*.xml) do call ImportScans.bat -q -s %SERVER% %DATABASE% %LOGDIR% "%%f"
for %%f in (%LOGDIR%\Sum_*.xml) do call ImportScans.bat -q -s %SERVER% %DATABASE% %LOGDIR% "%%f"
for %%f in (%LOGDIR%\File_*.xml) do call ImportScans.bat -q -s %SERVER% %DATABASE% %LOGDIR% "%%f"
for %%f in (%LOGDIR%\Error_*.xml) do call ImportScans.bat -q -s %SERVER% %DATABASE% %LOGDIR% "%%f"
for %%f in (%LOGDIR%\Scan_*.cab) do call ImportScans.bat -q -s -x %SERVER% %DATABASE% %LOGDIR% "%%f" 

if '%FILESPROCESSED%' == '0' goto LNoScanXML
cscript.exe /NoLogo .\Include\Import.wsf %SERVER% %DATABASE% -postscans
IF %ERRORLEVEL% NEQ 0 (
	goto LError
)
@echo Creating database indexes...
osql.exe -S %SERVER% -d %DATABASE% -n -h-1 -b -E -i .\Include\CreateIndexes.sql
IF %ERRORLEVEL% NEQ 0 (
	@echo Failed to created indexes
	goto OSQLError
)

@echo. 
REM Updating the Process_Control table; marking the bit ImportInProgress as OFF
osql.exe -S %SERVER% -d %DATABASE% -n -h-1 -E -b -Q "Update Process_Control Set ImportInProgress = 0" > nul 
IF %ERRORLEVEL% NEQ 0 (
	@echo Failed to set the ImportInProgress bit to 0
	goto OSQLError
) 

@echo Import operation complete.
goto LOperationComplete


:LNoScanXML
REM Updating the Process_Control table; marking the bit ImportInProgress as OFF
osql.exe -S %SERVER% -d %DATABASE% -n -h-1 -E -b -Q "Update Process_Control Set ImportInProgress = 0" > nul
IF %ERRORLEVEL% NEQ 0 (
	@echo Failed to set the ImportInProgress bit to 0
	goto OSQLError
) 
@echo No Scan XML was found to import. 
@echo.
@echo Scan XML must exist in the ^<PathToLogFile^> folder and Scan
@echo XML file names must begin with "Error_", "File_", "Scan_" or "Sum_".
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
if not '%5'=='' goto LInvalidArg

set SERVER=%1
set DATABASE=%2
set LOGDIR="%~f3"
set LOGFILE="%~f4"
set IMPORTEDDIR=%LOGDIR%\OMPMImported
if not exist %IMPORTEDDIR% mkdir %IMPORTEDDIR%
if not exist %IMPORTEDDIR% @echo ERROR: Cannot create %IMPORTEDDIR%. & goto LError

if '%EXTRACT%'=='1' goto LExtractAndImport

:LImport
@echo Importing file %LOGFILE%...
cscript.exe /NoLogo .\Include\Import.wsf %SERVER% %DATABASE% .\Schemas\LogFileMapping.xml %LOGFILE% -scans
if not '%ERRORLEVEL%'=='0' goto LError
move %LOGFILE% %IMPORTEDDIR% 1>nul
goto LOperationComplete

:LExtractAndImport
set FILESPROCESSED=1
set EXTRACTDIR=%LOGDIR%\OMPMExtracted
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
	call :LSubRemoveDir %EXTRACTDIR%
	goto LExpandError
)
@echo Importing extracted data...
cscript.exe /NoLogo .\Include\Import.wsf %SERVER% %DATABASE% .\Schemas\LogFileMapping.xml %EXTRACTDIR% -scans -bulk
if not '%ERRORLEVEL%'=='0' (
	call :LSubRemoveDir %EXTRACTDIR%
	goto LError
)
move %LOGFILE% %IMPORTEDDIR% 1>nul
call :LSubRemoveDir %EXTRACTDIR%
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

:LError
@echo.
goto LDone

:OSQLError
@echo An error occurred while attempting to run osql...
@echo Aborting program.
REM Resetting the ImportInProgress bit to OFF
osql.exe -S %SERVER% -d %DATABASE% -n -h-1 -E -Q "Update Process_Control Set ImportInProgress = 0" 
goto LDone

:InProgress
@echo According to data in the database another import process is in progress. 
@echo Only one import may be run at a time or the database may be corrupted.
@echo Please finish the prior import before beginning a new one.
@echo.
@echo If imports are not in process but were interrupted instead,
@echo it is safe to reset the ImportInProgress bit and restart the import.
@echo To reset the ImportInProgress bit, run the following at the command prompt:
@echo.
@echo osql.exe -S %SERVER% -d %DATABASE% -n -h-1 -E -Q"Update Process_Control Set ImportInProgress = 0" 
@echo.
pause
goto LDone

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
set TimeoutSeconds=
set MaxTime=
endlocal
goto LError

:LExitRetryAttempt
set TimeoutSeconds=
set MaxAttempt=
endlocal
goto LDone


:LInvalidArg
@echo ERROR: Invalid parameter usage.
@echo.

:LUsage
@echo USAGE:    ImportScans.bat ServerName DatabaseName PathToLogFile
@echo.
@echo EXAMPLE:  ImportScans.bat SQL001 OMPM c:\logfiles
@echo.
@echo Note: you must have read/write/create 
@echo permissions to the ^<PathToLogFile^> folder
@echo.
@echo Please see the Microsoft Office Migration 
@echo Planning Manager documentation for further
@echo information.
@echo.

:LDone
