@echo off
REM End-to-end test script for element CLI operations (Windows)
REM Prerequisites: Rhapsody must be running with an open project
REM Usage: scripts\test_element_cli_e2e.bat

setlocal enabledelayedexpansion

set CLI=python -m rhapsody_cli.cli.main
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set today=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set now=%%a%%b)
set CLASS_NAME=TestClass_%today%_%now%

echo ========================================
echo Element CLI E2E Test
echo ========================================
echo.

REM Step 1: List elements before adding
echo [Step 1] Query existing elements...
%CLI% element query
if %ERRORLEVEL% NEQ 0 (
    echo X Query failed
    exit /b 1
)
echo ✓ Query succeeded
echo.

REM Step 2: Add a new class
echo [Step 2] Adding new class: %CLASS_NAME%...
%CLI% element add --type class --name "%CLASS_NAME%"
if %ERRORLEVEL% NEQ 0 (
    echo X Add failed
    exit /b 1
)
echo ✓ Class added successfully
echo.

REM Step 3: Query and verify
echo [Step 3] Verifying class exists in project...
%CLI% element query | findstr "%CLASS_NAME%" >nul
if %ERRORLEVEL% NEQ 0 (
    echo X ERROR: Class not found in query results
    exit /b 1
)
echo ✓ Class '%CLASS_NAME%' found in query results
echo.

REM Step 4: Delete the class
echo [Step 4] Deleting class: %CLASS_NAME%...
%CLI% element delete --path "Root::%CLASS_NAME%"
if %ERRORLEVEL% NEQ 0 (
    echo X Delete failed
    exit /b 1
)
echo ✓ Class deleted successfully
echo.

REM Step 5: Verify deletion
echo [Step 5] Verifying class was deleted...
%CLI% element query | findstr "%CLASS_NAME%" >nul
if %ERRORLEVEL% EQU 0 (
    echo X ERROR: Class still found (deletion may have failed)
    exit /b 1
)
echo ✓ Class '%CLASS_NAME%' no longer in query results
echo.

echo ========================================
echo ✓ All E2E tests PASSED!
echo ========================================

endlocal
