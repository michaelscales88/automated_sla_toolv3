@echo off
if /i '%1'=='-q' shift& goto LParseArgs
if /i '%1'=='/q' shift& goto LParseArgs
@echo.
@echo Microsoft Office Migration Planning Manager version 1.0
@echo Export Tool
@echo Copyright (c) 2006 Microsoft Corporation.  All Rights Reserved.
@echo.

:LParseArgs
if '%1'=='-?' goto LUsage
if '%1'=='/?' goto LUsage
if /i '%1'=='help' goto LUsage
if /i '%1'=='-help' goto LUsage
if /i '%1'=='/help' goto LUsage

REM ----------------------------------------------------------------------
REM Export All
REM ----------------------------------------------------------------------
:LExport
if '%1'=='' goto LInvalidArg
if '%2'=='' goto LInvalidArg
if '%3'=='' goto LInvalidArg
set SERVER=%1
set DATABASE=%2
set OUTDIR=%~f3
set OUTDIR="%OUTDIR%"

if not exist %OUTDIR% mkdir %OUTDIR%
if not exist %OUTDIR% @echo ERROR: Cannot create %OUTDIR%. & goto LError
for %%f in (%OUTDIR%\*) do (
	@echo Warning: You are exporting to a folder that is not empty. 
	@echo Any file lists already in this folder will be combined with the files in the file list you are exporting.
	@echo.
	@echo Note that file lists are not merged, so you should only combine mutually exclusive file lists. Otherwise, files that are specified multiple times will be processed multiple times by tools using the file list folder.
:LAskContinue
	set /p USERIN=Do you want to export anyway? [yes] or [no]: 
	goto LAsked
:LAsked
	@echo.
	if /i not '%USERIN%'=='y' (
		if /i not '%USERIN%'=='yes' (
			if /i not '%USERIN%'=='n' (
				if /i not '%USERIN%'=='no' (
					@echo USERIN: '%USERIN%'
					@echo Invalid input.
					goto LAskContinue
				)
			)
			set USERIN=
			goto LDone
		)
	)
)
set USERIN=

if not '%4'=='' goto LExportSpecific

cscript.exe /NoLogo .\Include\Export.wsf %SERVER% %DATABASE% %OUTDIR%
if not '%ERRORLEVEL%'=='0' goto LError
@echo File list export successful.
goto LOperationComplete

REM ----------------------------------------------------------------------
REM Export for a specific Computer and User
REM ----------------------------------------------------------------------
:LExportSpecific
set DOMAIN=
set COMPUTER=
set FILTERID=
:LExportSpecificBody

if '%4'=='' goto LInvalidArg
if '%5'=='' goto LInvalidArg

if not '%4'=='/w' goto LDomainAndComputer
set FILTERID=/w %5
shift
shift
if '%4'=='' goto LExportFull

:LDomainAndComputer 
set DOMAIN=%4
set COMPUTER=%5
shift
shift
if not '%4'=='' goto LExportSpecificBody

:LExportFull

cscript.exe /NoLogo .\Include\Export.wsf %SERVER% %DATABASE% %OUTDIR% %DOMAIN% %COMPUTER% %FILTERID%
if not '%ERRORLEVEL%'=='0' goto LError
@echo File list export successful.
goto LOperationComplete



:LOperationComplete
@echo.
goto LPause

:LError
@echo.
goto LPause

:LInvalidArg
@echo ERROR: Invalid parameter usage.
@echo.

:LUsage
@echo USAGE:    Export.bat ServerName DatabaseName OutputFolder [DomainName ComputerName] [/w FilterId]
@echo.
@echo EXAMPLE:  Export.bat SQL001 OMPM c:\outputfilelist
@echo               or
@echo           Export.bat SQL001 OMPM c:\outputfilelist corpnet computer001
@echo               or
@echo           Export.bat SQL001 OMPM c:\outputfilelist /w 14
@echo.
@echo Note: you must have read/write/create 
@echo permissions to the <Output> folder
@echo.
@echo Please see the Microsoft Office Migration 
@echo Planning Manager documentation for further
@echo information.
@echo.
goto LDone

:LPause
pause

:LDone
  