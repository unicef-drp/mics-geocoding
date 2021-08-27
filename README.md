# Mics Geocode

This document is aimed at describing the project and helping developer at onboarding.

This document is **NOT** a comitment to anything. It is **NOT** an official technical specifications.

Author: Jan Burdziej, Unicef
Support in dev: Etienne Delclaux, CartONG

> In this project, MGP is used as an acornym for Mics Geocode Plugin

- [release notes](release-notes.md)

## Project structure description

There are three helpers script for windows:

### WIN_copy.bat

This script setup locally the qgis plugin. It copies everything at the right place in the qgis plugin directory
`%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\micsgeocodeplugin`

This is made for development phase and personal setup.

> The first time the plugin is copied using WIN_copy.bat, it is loaded but not activated. This has to be don in QGIS:
> `Plugin/Install or manage the extension` then `All` then search for `micsgeocode`
> Finally, check the checkbox, and it's all set !

### WIN_zip.bat

This script setup a zip file based on `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\micsgeocodeplugin`.
The zip file is named `micsgeocodeplugin.zip`, and will be located in the same folder as the WIN_zip.bat.
This is made to share the project with others.
For more information on this, please refer to the [official documentation on this topic](https://docs.qgis.org/3.16/fr/docs/user_manual/plugins/plugins.html#the-install-from-zip-tab)

> This script is based on the very common 7zip.
> Make sure this lib is installed before running this script.

### Plugin

For more information on this, please refer to the [official documentation on qgis plugin development](https://docs.qgis.org/3.16/en/docs/pyqgis_developer_cookbook/plugins/plugins.html#writing-a-plugin)

Here’s the directory structure the plugin:

```
├───icon_bars.png
├───icon_bg_w.png
├───icon_gis.png
├───icon_nobg.png
├───logo_bg_w.png
├───logo_nobg.png
├───logo_w-unicef.png
├───logo_wo-unicef.png
├───metadata.txt
├───mgp_config_reader.py
├───mgp_config_writer.py
├───mgp.py
├───mgp_dialog.py
├───mgp_dialog.ui
├───mgp_main_window.py
├───mgp_version.py
├───resources.py
├───resources.qrc
├───ui_mgp_dialog.py
├───WIN_build.bat
├───__init__.py
└───test
```

**init**.py = The starting point of the plugin. It has to have the classFactory() method and may have any other initialisation code.

- `png files` options for the logo and the icon used in the plugin
- `metadata.txt` Contains general info, version, name and some other metadata used by plugins website and plugin infrastructure
- `resources.qrc` The .xml document created by Qt Designer. Contains relative paths to resources of the forms.
- `resources.py` The translation of the .qrc file described above to Python.
- `mgp_dialog.ui` The GUI created by Qt Designer
- `ui_mgp_dialog.py` The translation of the form.ui described above to Python
- `mgp.py` The main working code of the plugin. Contains all the information about the actions of the plugin and the main code.
- `mgp_xxx.py` those are the code base behind the plugin. If some modifications needs to be developped on the plugin, those are the files to focus on
- `WIN_build.bat`: This helper scripts do the transciprtion from ui to py file, and qrc to py.
  **It needs to be executed only when modifications have been applied to the qrc or the ui file**

> The WIN_build.bat launch two commands, **pyuic5** and **pyrcc5**. They have to be installed first:

```
pip install pyqt5-tools
```

- `mgp_version.py` contains the version number of the plugin (also written in metadata.txt)
- `mgp_config_reader.py` read a config file (basic ini file) and initialize the plugin with it
- `mgp_config_writer.py` write a config file (basic ini file) based on the plugin interface
- `mgp_main_window.py` This is the part that handles all the complexity of the plugin interface. The signal/slot connection, etc.
  This documentation can't be a complete introduction to Qt interface programmation.
  Basically, this file helps maanging user inputs, testing values, and starts the processes.
  In order to the run the processes, it triggeres the Step01Manager and CovariatesProcesser contains in the **micsgeocode folder**

### MicsGeoCode

- `__init__.py` mandatory files for this folder to be used as a package
- `Logger.py` helper class that handle all the logging part. This trigger a logging inside the QGis Log Pannel
- `Transforms.py` helper class that contains only crs variables. This helps centralize every crs related var in one place.
- `Utils.py` this class manage some generic qgis layer processes, such as names, create/remove, write
- `ReferenceLayer.py` Facade that handle management of reference layer
- `CentroidsLoader.py` The **Centroids Loading** part: init, and process
- `CentroidsDisplacer.py` The **Centroids Displacment** part: init, and process
- `CovariatesProcesser.py` Step02 algorithm

The code is documented, more precise informations would be found inside the files.
