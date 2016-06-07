@echo off
if /i "%1"=="-q" shift& goto LParseArgs
if /i "%1"=="/q" shift& goto LParseArgs
@echo.
@echo Microsoft Office Migration Planning Manager version 1.0
@echo Database Deprovisioning Tool
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

cscript.exe /NoLogo .\Include\DeleteDB.wsf %SERVER% %DATABASENAME%
if not "%ERRORLEVEL%"=="0" goto LError

:LOperationComplete
@echo Database '%DATABASENAME%' was deleted successfully.
@echo.
goto LDone

:LError
@echo.
goto LDone

:LInvalidArg
@echo ERROR: Invalid parameter usage.
@echo.

:LUsage
@echo USAGE:    DeleteDB.bat ServerName DatabaseName
@echo.
@echo EXAMPLE:  DeleteDB.bat SQL001 OMPM
@echo.
@echo Please see the Microsoft Office Migration
@echo Planing Manager documentation for further
@echo information.
@echo.

:LDone
    
