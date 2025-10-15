# Release Notes

## 1.3.0
 
### Features
 
- For geospatial covariates calculation, produce outputs consistent with the QGIS Zonal Statistics approach.
- For displacement, more consistent buffer radius across different latitudes (UTM projection).
- Support for specifying a NoData value in the covariates input CSV and default variable names for the “Boundary layer” dropdown.
- Add the Admin drop-down list to the “Displace” tab.
- Move the “Generate Centroid Buffers” button from “Displace” to “Generate,”.
- Reposition the “Generate Centroids” button.
 
### Bugfixes
 
- Rename outputs correctly when using original buffers.
- Correct the file dialog label for the cluster source input.
- Prevent unintended use of previous basenames.
- Stop saving temporary “distance to nearest shp” layers.
 
## Previous to 1.3.0
 
Notes are not available at the moment for intermediate releases.

## 0.9

### Features

- Path separator santdardized across the plugin
- Release notes document added
- Git history cleaned up

### Bugfixes

- Default ouput directory wasn't loaded at startup
- Update all the paths with new icon name (same icon, new filename)

## 0.8

> This document started at v0.9. The informations on the previous version are incomplete.

### Features

- Plugin moved to a separate toolbasr
- Name changed: MGP/Mics Geocode Plugin --> MICS GIS PLUGIN
- Dialog always appear at the center of the screen instead of 200,200

### Bugfixes

- Disable "reloadLayerFromDiskToAvoidMemoryFlag" --> memory flag still active. But this was an issue.

## 0.7

### Features

- ZIP Procedure documentation
- 'Micsgeocode_old' made compatible with 0.6
- Auto save of the Covariates shortest distance layer
- Field 'cluster' is dynamic on step3

### Bugfixes

- Dialog appear at 200,200: avoid any position miscalculation

## 0.6

First really functional version that include step1, step2, step3.
A lot of development has been going on for this version.

> To have more information on this, please refer to the git history.
