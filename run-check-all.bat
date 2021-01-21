@echo off
setlocal enableextensions enabledelayedexpansion

IF "%1"=="" (
    GOTO HAVE_0
)

REM filename: check a single file
set dirname=%1
echo filename=%dirname%
GOTO CONT

:HAVE_0
set dirname=clmutils
set dirname=hlm_texts
set dirname=vector_search

:CONT

echo %dirname%
echo.
echo ----------
echo call pyright.cmd %dirname%
call pyright.cmd %dirname%
REM if %ERRORLEVEL% NEQ 0 exit %ERRORLEVEL%

echo ----------
echo call flake8.bat %dirname%
call flake8.bat %dirname%
REM if %ERRORLEVEL% NEQ 0 exit %ERRORLEVEL%

echo ----------
echo black --diff %dirname%
black --diff %dirname%
REM if %ERRORLEVEL% NEQ 0 exit %ERRORLEVEL%

echo ----------
echo pylint %dirname%
pylint %dirname%
REM if %ERRORLEVEL% NEQ 0 exit %ERRORLEVEL%

REM skip pytest if single file
IF "%1"=="" (
    GOTO HAVE_0A
)
GOTO END

:HAVE_0A
echo ----------
echo pep257
pep257.exe

echo ----------
echo pylint tests
pylint tests
REM if %ERRORLEVEL% NEQ 0 exit %ERRORLEVEL%

GOTO END

:END