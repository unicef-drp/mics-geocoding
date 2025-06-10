
@ECHO OFF

@REM ##########################################################################
@REM set paths
@REM ##########################################################################

SET PROJECT_SOURCE_DIRECTORY="%cd%"

SET QGIS_PLUGIN_DIRECTORY=%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins
SET PLUGIN_DIRECTORY_NAME=micsgeocodeplugin
SET PLUGIN_DIRECTORY=%QGIS_PLUGIN_DIRECTORY%\%PLUGIN_DIRECTORY_NAME%\

ECHO "Qgis_plugins_directory: " %QGIS_PLUGIN_DIRECTORY%
ECHO "micsgeocode_plugin_directory: " %PLUGIN_DIRECTORY%

@REM ##########################################################################
@REM Create qgisplugin directory
@REM ##########################################################################

@REM RM previous plugin if exists

IF EXIST %PLUGIN_DIRECTORY% (
  ECHO "Previous version found !"
  RMDIR /S /Q %PLUGIN_DIRECTORY%
)

IF EXIST %PLUGIN_DIRECTORY% (
    ECHO "A problem occured. Leaving."
    EXIT /B
)

@REM create the plugin directory

MKDIR %PLUGIN_DIRECTORY%

IF NOT EXIST %PLUGIN_DIRECTORY% (
    ECHO "A problem occured. Leaving."
    EXIT /B
)

@REM ##########################################################################
@REM copy plugin
@REM ##########################################################################

set PLUGIN_SOURCE_DIRECTORY=%PROJECT_SOURCE_DIRECTORY%\plugin

set PLUGIN_DIRECTORIES=test

@REM all plugin related files
set PLUGIN_FILES=__init__.py
set PLUGIN_FILES=%PLUGIN_FILES%;icon_bars.png
set PLUGIN_FILES=%PLUGIN_FILES%;metadata.txt
set PLUGIN_FILES=%PLUGIN_FILES%;mgp_plugin.py
set PLUGIN_FILES=%PLUGIN_FILES%;ui_mgp_mainwindow.py
set PLUGIN_FILES=%PLUGIN_FILES%;mgp_main_window.py
set PLUGIN_FILES=%PLUGIN_FILES%;mgp_main_window_tab1handler.py
set PLUGIN_FILES=%PLUGIN_FILES%;mgp_main_window_tab2handler.py
set PLUGIN_FILES=%PLUGIN_FILES%;mgp_main_window_tab3handler.py
set PLUGIN_FILES=%PLUGIN_FILES%;mgp_config_reader.py
set PLUGIN_FILES=%PLUGIN_FILES%;mgp_config_writer.py
set PLUGIN_FILES=%PLUGIN_FILES%;mgp_file.py
set PLUGIN_FILES=%PLUGIN_FILES%;mgp_version.py
set PLUGIN_FILES=%PLUGIN_FILES%;resources_rc.py

FOR %%F IN (%PLUGIN_FILES%) DO (
    ROBOCOPY %PLUGIN_SOURCE_DIRECTORY% %PLUGIN_DIRECTORY% %%F /NJH /NJS /NC /NS /NP /NFL /NDL
)

@REM ##########################################################################
@REM copy mcis geocode INSIDE plugin directory
@REM ##########################################################################

set MICS_SOURCE_DIRECTORY=%PROJECT_SOURCE_DIRECTORY%\plugin\micsgeocode

ROBOCOPY %MICS_SOURCE_DIRECTORY% %PLUGIN_DIRECTORY%\micsgeocode /S /E /NJH /NJS /NC /NS /NP /NFL /NDL

@REM ##########################################################################
@REM remark on parametre copy
@REM ##########################################################################

@REM /NFL : No File List - don't log file names.
@REM /NDL : No Directory List - don't log directory names.
@REM /NJH : No Job Header.
@REM /NJS : No Job Summary.
@REM /NP  : No Progress - don't display percentage copied.
@REM /NS  : No Size - don't log file sizes.
@REM /NC  : No Class - don't log file classes.

@ECHO ON