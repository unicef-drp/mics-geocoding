# MICS Geocode Plugin

A QGIS plugin for geocoding and processing Multiple Indicator Cluster Survey (MICS) data with privacy-preserving displacement and covariate extraction.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![QGIS: 3.0+](https://img.shields.io/badge/QGIS-3.0+-green.svg)](https://qgis.org)

---

## Quick Links

- 📖 **[User Guide](USER_GUIDE.md)** - Complete tutorials and usage instructions
- 🔧 **[Developer Documentation](#developer-documentation)** - Technical implementation details
- 📝 **[Release Notes](release-notes.md)** - Version history and changes
- 🐛 **[Report Issues](https://github.com/unicef/mics-geocoding/issues)** - Bug reports and feature requests

---

## What is This Plugin?

The MICS GIS Plugin streamlines the geocoding workflow for UNICEF's Multiple Indicator Cluster Surveys. It automates three critical tasks:

1. **📍 Centroid Loading** - Import GPS coordinates from CSV files or existing shapefiles
2. **🔒 Privacy Protection** - Apply controlled displacement to protect respondent anonymity
3. **🌍 Covariate Extraction** - Extract environmental and infrastructure data for spatial analysis

### Key Features

- **Flexible Input**: Accepts CSV (with lat/lon) or shapefile formats
- **Automated Processing**: Streamlined workflow with minimal manual intervention
- **Privacy-Aware**: Built-in displacement algorithms for data anonymization
- **Covariate Processing**: Extract data from multiple raster and vector layers
- **Configuration Management**: Save and reload project settings
- **QGIS Integration**: Seamless integration with QGIS processing framework

---

## Quick Start

### For Users

If you just want to **use** the plugin:

1. Download the latest release from `releases/micsgeocodeplugin-[version].zip`
2. In QGIS: `Plugins` → `Manage and Install Plugins` → `Install from ZIP`
3. Follow the **[User Guide](USER_GUIDE.md)** for step-by-step tutorials

### For Developers

If you want to **develop** or **modify** the plugin, see the [Developer Documentation](#developer-documentation) below.

---

## System Requirements

- **QGIS**: Version 3.0 or higher (3.16+ recommended)
- **Python**: 3.6+ (bundled with QGIS)
- **Operating System**: Windows, macOS, or Linux
- **Dependencies**: All required packages included with QGIS

---

## Documentation

### User Documentation

- **[Complete User Guide](USER_GUIDE.md)** - Installation, tutorials, troubleshooting
  - What the plugin does and who should use it
  - Step-by-step installation instructions
  - Tutorial 1: Loading centroids from CSV
  - Tutorial 2: Loading centroids from shapefile
  - Tutorial 3: Processing covariates
  - Input/output format specifications
  - Troubleshooting common issues
  - FAQ

### Developer Documentation

### Developer Documentation

The information below is for developers who want to modify or contribute to the plugin.

**Authors**: Jan Burdziej (UNICEF), Nazim Gashi (UNICEF), Etienne Delclaux (CartONG)

> **Note**: MGP is used throughout the codebase as an acronym for MICS Geocode Plugin

---

## Project Structure

The repository is organized as follows:

```
mics-geocoding/
├── plugin/                    # Main plugin code
│   ├── micsgeocode/          # Core processing modules
│   ├── *.py                  # UI and configuration handlers
│   ├── *.ui                  # Qt Designer interface files
│   ├── metadata.txt          # Plugin metadata
│   └── resources.qrc         # Qt resources
├── releases/                  # Packaged plugin releases
├── WIN_copy.bat              # Windows: Install to QGIS plugins folder
├── WIN_zip.bat               # Windows: Create distributable ZIP
├── README.md                 # This file
├── USER_GUIDE.md             # End-user documentation
└── release-notes.md          # Version history
```

---

## Development Setup

### Prerequisites

- QGIS 3.0+ installed
- Python 3.6+ (bundled with QGIS)
- Qt Designer (optional, for UI modifications)
- 7zip (for creating release packages)

### Windows Development Workflow

Three helper scripts are provided for Windows developers:

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
├───mgp_mainwindow.ui
├───mgp_main_window.py
├───mgp_version.py
├───resources.py
├───resources.qrc
├───ui_mgp_mainwindow.py
├───WIN_build.bat
├───__init__.py
└───test
```

**init**.py = The starting point of the plugin. It has to have the classFactory() method and may have any other initialisation code.

- `png files` options for the logo and the icon used in the plugin
- `metadata.txt` Contains general info, version, name and some other metadata used by plugins website and plugin infrastructure
- `resources.qrc` The .xml document created by Qt Designer. Contains relative paths to resources of the forms.
- `resources.py` The translation of the .qrc file described above to Python.
- `mgp_mainwindow.ui` The GUI created by Qt Designer
- `ui_mgp_mainwindow.py` The translation of the *.ui described above to Python
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

### MICS GeoCode

- `__init__.py` mandatory files for this folder to be used as a package
- `Logger.py` helper class that handle all the logging part. This trigger a logging inside the QGis Log Pannel
- `Transforms.py` helper class that contains only crs variables. This helps centralize every crs related var in one place.
- `Utils.py` this class manage some generic qgis layer processes, such as names, create/remove, write
- `ReferenceLayer.py` Facade that handle management of reference layer
- `CentroidsLoader.py` The **Centroids Loading** part: init, and process
- `CentroidsDisplacer.py` The **Centroids Displacment** part: init, and process
- `CovariatesProcesser.py` Step02 algorithm

The code is documented, more precise informations would be found inside the files.
