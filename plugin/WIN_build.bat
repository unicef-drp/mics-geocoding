@ECHO OFF

@REM set paths

SET PLUGIN_RESOURCES_FILENAME=resources.qrc
SET PLUGIN_SOURCE_DIRECTORY=%cd%

SET PLUGIN_RESOURCES_FILE=%PLUGIN_SOURCE_DIRECTORY%\resources.qrc

@REM run pyuic (not needed here, th eui file is loaded directly)
pyuic5.exe %PLUGIN_SOURCE_DIRECTORY%\mics_geocode_plugin_dialog.ui -o %PLUGIN_SOURCE_DIRECTORY%\ui_mics_geocode_plugin_dialog.py

@REM run pyrcc

pyrcc5.exe %PLUGIN_SOURCE_DIRECTORY%\resources.qrc -o %PLUGIN_SOURCE_DIRECTORY%\resources.py

@ECHO ON