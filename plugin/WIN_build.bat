@ECHO OFF

@REM set paths

SET PLUGIN_RESOURCES_FILENAME=resources.qrc
SET PLUGIN_SOURCE_DIRECTORY=%cd%

SET PLUGIN_RESOURCES_FILE=%PLUGIN_SOURCE_DIRECTORY%\resources.qrc

@REM run pyuic (not needed here, th eui file is loaded directly)
pyuic5.exe %PLUGIN_SOURCE_DIRECTORY%\mgp_mainwindow.ui -o %PLUGIN_SOURCE_DIRECTORY%\ui_mgp_dialog.py

@REM run pyrcc

pyrcc5.exe %PLUGIN_SOURCE_DIRECTORY%\resources.qrc -o %PLUGIN_SOURCE_DIRECTORY%\resources.py

@ECHO ON