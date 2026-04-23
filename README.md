# MICS Geocode Plugin

A QGIS plugin designed to support the Multiple Indicator Cluster Survey (MICS) geospatial data anonymisation and extraction of geospatial covariates.
Although designed for MICS, the Plugin can be used for any household survey.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![QGIS: 3.0+](https://img.shields.io/badge/QGIS-3.0+-green.svg)](https://qgis.org)

---

## Quick Links

- 📖 **[User Guide](USER_GUIDE.md)** - Usage instructions
- 🔧 **[Developer Documentation](#developer-documentation)** - Technical implementation details
- 📝 **[Release Notes](release-notes.md)** - Version history and changes
- 🐛 **[Report Issues](https://github.com/unicef/mics-geocoding/issues)** - Bug reports and feature requests

---

## What is This Plugin?

The MICS Geocode Plugin streamlines the processing of GIS data for MICS surveys. Following documented methodolgy (https://mics.unicef.org/publications/mics-methodological-paper-no-12-2024-geographic-displacement-procedures-and AND https://mics.unicef.org/publications/mics-methodological-paper-no-13-2025-geospatial-covariates-extraction-procedures), it automates three key tasks:

1. **📍 Centroid Generation** - Generate cluster centroids from GPS coordinates in shapefiles or CSV files
2. **🔒 Privacy Protection** - Apply random displacement to ensure respondent anonymity
3. **🌍 Covariate Extraction** - Extract geospatial covariates from raster and vector datasets for further analysis

### Key Features

- **Flexible Input**: Accepts CSV (with lat/lon) or shapefile formats
- **Automated Processing**: Streamlined workflow with minimal manual intervention
- **Respondent Protection**: Built-in displacement algorithms for data anonymisation
- **Covariate Processing**: Extract data from multiple raster and vector layers
- **Configuration Management**: Save and reload project settings
- **QGIS Integration**: Seamless integration with QGIS processing framework

---

## Quick Start

### For Users

For more detailed instructions on how to install and use the plugin, go to the MICS website (https://mics.unicef.org/mics-gis#learning_corner):
1. Download the latest version of the plugin
2. Download the manual on how to install the plugin
3. Download the manual on how to use the plugin

The MICS tools are available in the UN languages and can be accessed at https://mics.unicef.org/tools#survey-design

### For Developers

If you want to **develop** or **modify** the plugin, see the [Developer Documentation](#developer-documentation) below.

---

## System Requirements

- **QGIS**: Version 3.0+
- **Python**: 3.6+ (bundled with QGIS)
- **Operating System**: Windows, macOS, or Linux
- **Dependencies**: All required packages included with QGIS

---

## Documentation

### User Documentation

- **[Complete User Guide](USER_GUIDE.md)**

### Developer Documentation

The information below is for developers who want to modify or contribute to the plugin.

**Authors**: Nazim Gashi (UNICEF), Jan Burdziej (UNICEF), Etienne Delclaux (CartONG), Miguel Moreno (CartONG)

> **Note**: MGP is used throughout the codebase as an acronym for MICS Geocode Plugin

---

## Project structure description

```
├── plugin/
│   ├── __init__.py
│   ├── icon_bars.png
│   ├── icon_gis.png
│   ├── logo_w-unicef.png
│   ├── logo_wo-unicef.png
│   ├── metadata.txt
│   ├── mgp_config_reader.py
│   ├── mgp_config_writer.py
│   ├── mgp_file.py
│   ├── mgp_main_window_tab1handler.py
│   ├── mgp_main_window_tab2handler.py
│   ├── mgp_main_window_tab3handler.py
│   ├── mgp_main_window.py
│   ├── mgp_mainwindow.ui
│   ├── mgp_plugin.py
│   ├── mgp_version.py
│   ├── resources_rc.py
│   ├── resources.qrc
│   ├── ui_mgp_mainwindow.py
│   ├── WIN_build.bat
│   └── micsgeocode/
│       ├── __init__.py
│       ├── CentroidBuffersLayerWriter.py
│       ├── CentroidBuffersMaxDistanceComputer.py
│       ├── CentroidsDisplacer.py
│       ├── CentroidsLoader.py
│       ├── CovariatesProcesser.py
│       ├── Errors.py
│       ├── Logger.py
│       ├── ProgressBar.py
│       ├── ReferenceLayer.py
│       ├── Transforms.py
│       ├── UrbanismValidator.py
│       ├── Utils.py
│       └── test/
├── releases/
├── README.md
├── release-notes.md
├── WIN_copy.bat
├── WIN_zip.bat
```

## Development environment

### User interface

User interface (`mgp_mainwindow.ui` file) is designed in Qt Designer. Run [`WIN_build.bat`](#win_buildbat) to generate the Python file (`ui_mgp_mainwindow.py`).

### Using VS Code

Followed the solution in https://aneto.pt/posts/tutorials/2024-05-11-create-easy-pyqgis-developement-environment-using-conda-and-vscode/.

> \\!/ Important note: The batch file used to compile UI files (from .ui to .py), `WIN_build.bat`, contains dependencies not working with the latest Python versions (as of June 2025). When installing a conda environment for QGIS, use Python version `3.9.22`.

```
conda create -n qgis_dev_p39 qgis python=3.9.22 -c conda-forge
```

Being `qgis_dev_p39` the name of the environment (includes the python version to better identify it).

### Plugin

For more information on this, please refer to the [official documentation on qgis plugin development](https://docs.qgis.org/3.16/en/docs/pyqgis_developer_cookbook/plugins/plugins.html#writing-a-plugin).

- **`init.py`**: The starting point of the plugin. It has to have the classFactory() method and may have any other initialisation code.
- `png files`: options for the logo and the icons used in the plugin.
- `metadata.txt`: Contains general info, version, name and some other metadata used by plugins website and plugin infrastructure.
- `resources.qrc`: The .xml document created by Qt Designer. Contains relative paths to resources of the forms.
- `resources_rc.py`: The translation of the .qrc file described above to Python (created by `WIN_build.bat`).
- `mgp_mainwindow.ui`: The GUI created by Qt Designer.
- `ui_mgp_mainwindow.py`: The translation of the *.ui described above to Python (created by `WIN_build.bat`).
- `mgp_plugin.py`: The main working code of the plugin. Contains all the information about the actions of the plugin and the main code.
- `mgp_xxx.py`: those are the code base behind the plugin. If some modifications needs to be developped on the plugin, those are the files to focus on.
- `mgp_version.py`: contains the version number of the plugin (also written in metadata.txt).
- `mgp_config_reader.py`: read a config file (basic ini file) and initialize the plugin with it.
- `mgp_config_writer.py`: write a config file (basic ini file) based on the plugin interface.
- `mgp_main_window[_*].py`: This is the part that handles all the complexity of the plugin interface. The signal/slot connection, etc.
  This documentation can't be a complete introduction to Qt interface programmation.
  Basically, this file helps maanging user inputs, testing values, and starts the processes.
  In order to the run the processes, it triggeres the Step01Manager and CovariatesProcesser contains in the **micsgeocode folder**
- [`WIN_build.bat`](#win_buildbat): This helper script does the transcription from ui to py file, and qrc to py.
  **It needs to be executed only when modifications have been applied to the qrc or the ui file**
- [micsgeocode/](#mics-geocode-folder): folder with dedicated processes of MICS GeoCode  

### MICS GeoCode folder

- `__init__.py`: Mandatory file for this folder to be used as a package
- `CentroidBuffersLayerWriter.py`: Creates buffer layers anonymization purposes.
- `CentroidBuffersMaxDistanceComputer.py`: Calculates the maximum centroid buffer radius.
- `Logger.py`: Helper class that handles all the logging part. This triggers a logging inside the QGis Log Pannel
- `Errors.py`: List of error codes and descriptions.
- `ReferenceLayer.py`: Facade that handles management of reference layer.
- `Transforms.py`: Helper class that handles UTM transformation.
- `UrbanismValidator.py`: Class that validates displacement constraints based on urbanisation degree raster classification.
- `Utils.py`: This class manages some generic qgis layer processes, such as names, create/remove, write.
- `CentroidsLoader.py`: The **Centroids Loading** part: init, and process.
- `CentroidsDisplacer.py`: The **Centroids Displacment** part: init, and process.
- `CovariatesProcesser.py`: Algorithm for the covariate **Extraction** part.
- `ProgressBar.py`: Manager for progress bar.

The code is documented, more precise informations would be found inside the files.

### Helper scripts for windows (.bat files)

There are three helper scripts for windows. Run them in the [conda environment](#using-vs-code) created for the purpose.

#### WIN_build.bat

This helper scripts do the transciprtion from ui to py file, and qrc to py.

**It needs to be executed only when modifications have been applied to the qrc or the ui file**

> The WIN_build.bat launch two commands, **pyuic5** and **pyrcc5**. They have to be installed first:

```
pip install pyqt5-tools
```

#### WIN_copy.bat

This script setup locally the qgis plugin. It copies everything at the right place in the qgis plugin directory
`%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\micsgeocodeplugin`

This is made for development phase and personal setup.

> The first time the plugin is copied using WIN_copy.bat, it is loaded but not activated. This has to be don in QGIS:
> `Plugin/Install or manage the extension` then `All` then search for `micsgeocode`
> Finally, check the checkbox, and it's all set!

#### WIN_zip.bat

This script setup a zip file based on `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\micsgeocodeplugin`.
The zip file is named `micsgeocodeplugin.zip`, and will be located in the same folder as the WIN_zip.bat.
This is made to share the project with others.
For more information on this, please refer to the [official documentation on this topic](https://docs.qgis.org/3.16/fr/docs/user_manual/plugins/plugins.html#the-install-from-zip-tab).

> This script is based on the very common 7zip.
> Make sure this lib is installed before running this script.



