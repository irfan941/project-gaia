@echo off
:: Aria — Restore Script
:: Usage: restore.bat backups\aria_backup_2026-04-15_10-00-00.sql

if "%~1"=="" (
    echo Usage: restore.bat ^<backup_file^>
    echo Example: restore.bat backups\aria_backup_2026-04-15.sql
    pause
    exit /b 1
)

set BACKUP_FILE=%~1

if not exist "%BACKUP_FILE%" (
    echo ERROR: File not found: %BACKUP_FILE%
    pause
    exit /b 1
)

:: Find the running container
for /f "tokens=*" %%i in ('docker ps --filter "name=db" --filter "ancestor=pgvector/pgvector:pg16" --format "{{.Names}}" 2^>nul') do set CONTAINER=%%i

if "%CONTAINER%"=="" (
    echo ERROR: Aria database container not running.
    echo Run: docker-compose up -d db
    pause
    exit /b 1
)

echo.
echo ================================================
echo  Aria Restore
echo  File: %BACKUP_FILE%
echo  Container: %CONTAINER%
echo ================================================
echo.
echo WARNING: This will overwrite the current database!
set /p CONFIRM=Type YES to continue:

if /i not "%CONFIRM%"=="YES" (
    echo Cancelled.
    pause
    exit /b 0
)

echo Restoring...
docker exec -i %CONTAINER% psql -U postgres aria < "%BACKUP_FILE%"

if %ERRORLEVEL% == 0 (
    echo.
    echo SUCCESS! Database restored from %BACKUP_FILE%
) else (
    echo.
    echo ERROR: Restore failed.
)

pause
