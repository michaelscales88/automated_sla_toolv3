@echo off
if /i "%1"=="-q" shift& goto LParseArgs
if /i "%1"=="/q" shift& goto LParseArgs
@echo.
@echo Microsoft Office Migration Planning Manager version 1.0
@echo Database Provisioning Tool
@echo Copyright (c) 2006 Microsoft Corporation.  All Rights Reserved.
@echo.

:LParseArgs
if "%1"=="-?" goto LUsage
if "%1"=="/?" goto LUsage
if /i "%1"=="help" goto LUsage
if /i "%1"=="-help" goto LUsage
if /i "%1"=="/help" goto LUsage
if "%1"=="" goto LInvalidArg
if "%2"=="" goto LInvalidArg
if not "%3"=="" goto LInvalidArg

set SERVER=%1
set DATABASENAME=%2

cscript.exe /NoLogo .\Include\CreateDB.wsf %SERVER% %DATABASENAME%
if not "%ERRORLEVEL%"=="0" goto LError

:LOperationComplete
@echo Database '%DATABASENAME%' was created successfully.
@echo.
goto LDone

:LError
@echo.
goto LDone

:LInvalidArg
@echo ERROR: Invalid parameter usage.
@echo.

:LUsage
@echo USAGE:    CreateDB.bat ServerName DatabaseName
@echo.
@echo EXAMPLE:  CreateDB.bat SQL001 OMPM
@echo.
@echo Please see the Microsoft Office Migration
@echo Planning Manager documentation for further
@echo information.
@echo.

:LDone
    
