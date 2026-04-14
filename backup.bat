@echo off
:: Aria — Full Backup Script
:: Backs up PostgreSQL database to a timestamped .sql file
:: Run: backup.bat

set BACKUP_DIR=%~dp0backups
set TIMESTAMP=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%_%TIME:~0,2%-%TIME:~3,2%-%TIME:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set FILENAME=aria_backup_%TIMESTAMP%.sql

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

echo.
echo ================================================
echo  Aria Backup
echo  Output: backups\%FILENAME%
echo ================================================
echo.

:: Find the running container name
for /f "tokens=*" %%i in ('docker ps --filter "name=db" --filter "ancestor=pgvector/pgvector:pg16" --format "{{.Names}}" 2^>nul') do set CONTAINER=%%i

if "%CONTAINER%"=="" (
    echo ERROR: Aria database container not running.
    echo Make sure Docker is running and you have started: docker-compose up -d db
    pause
    exit /b 1
)

echo Found container: %CONTAINER%
echo Exporting database...

docker exec %CONTAINER% pg_dump -U postgres aria > "%BACKUP_DIR%\%FILENAME%"

if %ERRORLEVEL% == 0 (
    echo.
    echo SUCCESS! Backup saved to:
    echo   backups\%FILENAME%
    echo.
    echo To restore on a new device:
    echo   docker exec -i ^<container^> psql -U postgres aria ^< backups\%FILENAME%
) else (
    echo.
    echo ERROR: Backup failed. Check that Docker is running.
)

echo.
pause
