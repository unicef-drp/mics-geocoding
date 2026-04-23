# Release Notes

## 1.4.0

### Features

- Covariate CSV input format: it allows now several covariates for a single file in one row instead of the old (but still supported) one covariate-one row. Optimises the computation as all the covariates in the row are obtained at the same zonal stat function call. Summary Statistics and Variable Name columns must have the same number of elements, delimited by semicolons.
- CSV delimiters. The tool now autodetects the delimiters in the input CSV files. Instead of just comma (,), it also supports now semicolon (;), tab and pipe (|). When semicolon is used at CSV file level, the delimiter for the covariates in the previous point must be the comma.
- Application of pole of inaccessibility instead of centroids when possible. It uses now pole of inaccessibility for nearest distance calculation (as seen more logical when working with irregular polygons like admin areas instead of just buffers).
- Added progress bar for steps 2 (displace) and 3 (compute covariates).
- Added button to open displaced anonymised centroids CSV file in step 2.

### Bugfixes

- Pole of inaccessibility bug in CentroidsLoader (when loading multipoint clusters through CSV)
- Solved errors and warnings shown in Logs (when calling twice the centroid loader or the displacer)
- Replaced deprecated QgsField constructor using QVariant by QMetaType.Type


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
