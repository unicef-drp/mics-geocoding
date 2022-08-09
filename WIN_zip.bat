@ECHO OFF

@REM ##########################################################################
@REM set paths
@REM ##########################################################################

SET QGIS_PLUGIN_DIRECTORY=%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins

SET PLUGIN_DIRECTORY_NAME=micsgeocodeplugin

SET PLUGIN_DIRECTORY=%QGIS_PLUGIN_DIRECTORY%\%PLUGIN_DIRECTORY_NAME%\

SET ZIP_TARGET_DIRECTORY="%cd%"\%PLUGIN_DIRECTORY_NAME%-0.13.rc1.zip

@REM ##########################################################################
@REM set paths
@REM ##########################################################################


7z a -tzip %ZIP_TARGET_DIRECTORY% %PLUGIN_DIRECTORY%

@ECHO ON