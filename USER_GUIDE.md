# MICS GIS Plugin - User Guide

## Table of Contents

- [What is the MICS GIS Plugin?](#what-is-the-mics-gis-plugin)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Workflow Overview](#workflow-overview)
- [Step-by-Step Tutorials](#step-by-step-tutorials)
- [Input/Output Formats](#inputoutput-formats)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

---

## What is the MICS GIS Plugin?

The MICS GIS Plugin is a QGIS tool designed to streamline geocoding workflows for Multiple Indicator Cluster Surveys (MICS) conducted by UNICEF. It automates three key processes:

1. **Centroid Loading**: Import and process GPS coordinates or existing centroids from CSV or shapefile formats
2. **Displacement**: Apply displacement algorithms to protect respondent privacy while maintaining analytical utility
3. **Covariate Processing**: Extract geospatial covariates (environmental, infrastructure, etc.) for survey clusters

### Who Should Use This Plugin?

- MICS survey data managers
- GIS specialists working with survey data
- Researchers processing geocoded survey clusters
- Anyone needing to anonymize GPS coordinates while preserving spatial relationships

---

## System Requirements

### Minimum Requirements

- **QGIS Version**: 3.0 or higher
- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.6+ (bundled with QGIS)
- **Disk Space**: 100 MB for plugin and temporary processing files

### Recommended

- **QGIS Version**: 3.16 or higher (for optimal compatibility)
- **RAM**: 8 GB or more (for processing large datasets)
- **Python Packages**: All required packages are included with QGIS

### Required Data

- GPS coordinates (CSV format) or existing centroids (SHP format)
- Reference boundary layer (shapefile)
- Covariate raster or vector layers (optional, for Step 3)

---

## Installation

### Method 1: Install from ZIP (Recommended for Users)

1. **Download the Plugin**
   - Get the latest release from the `releases/` folder
   - Download `micsgeocodeplugin-[version].zip`

2. **Install in QGIS**
   - Open QGIS
   - Go to `Plugins` → `Manage and Install Plugins`
   - Click on the `Install from ZIP` tab
   - Browse to the downloaded ZIP file
   - Click `Install Plugin`

3. **Activate the Plugin**
   - Go to `Plugins` → `Manage and Install Plugins`
   - Click on the `Installed` tab
   - Search for "MICS GIS PLUGIN"
   - Check the checkbox to activate it

4. **Verify Installation**
   - You should see a new toolbar with the MICS GIS icon
   - Click the icon to open the plugin interface

### Method 2: Manual Installation (For Developers)

See the main [README.md](README.md) for development installation instructions.

---

## Getting Started

### Quick Start (5 Minutes)

This quick tutorial will help you verify the plugin is working correctly.

1. **Open the Plugin**
   - Click the MICS GIS toolbar icon
   - The plugin window will open with three tabs

2. **Configure Output Settings**
   - Enter a basename for your project (e.g., "mics_survey_2024")
   - Select an output directory for results

3. **Save Configuration**
   - Click `File` → `Save` to save your settings
   - This creates a `.mgc` configuration file you can reload later

### Understanding the Interface

The plugin has **three main tabs**, corresponding to the three processing steps:

- **Tab 1: Centroids Loading & Displacement** - Import and anonymize GPS coordinates
- **Tab 2: Covariate Processing** - Extract environmental and infrastructure data
- **Tab 3: Reference Layer Management** - Configure boundary layers

---

## Workflow Overview

### Typical Processing Workflow

```
┌─────────────────────────────────┐
│  Step 1: Load GPS Coordinates   │
│  (CSV or Shapefile)              │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Step 2: Apply Displacement     │
│  (For Privacy Protection)        │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Step 3: Process Covariates     │
│  (Extract Spatial Data)          │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Output: Anonymized Geocoded    │
│  Data with Covariates            │
└─────────────────────────────────┘
```

### Configuration Files

The plugin uses `.mgc` configuration files to save your settings:
- File paths to input data
- Field mappings
- Processing parameters
- Output directories

**Tip**: Save your configuration after setup so you can reload it for similar projects.

---

## Step-by-Step Tutorials

### Tutorial 1: Loading Centroids from CSV

This tutorial demonstrates loading GPS coordinates from a CSV file.

#### Prerequisites
- A CSV file with GPS coordinates
- Columns for: cluster number, latitude, longitude, cluster type

#### Steps

1. **Open Tab 1: Centroids Source**

2. **Select Input File**
   - Click `Browse` next to "Centroids Source File"
   - Select your CSV file

3. **Map Fields**
   - **Cluster Number**: Select the column with unique cluster IDs
   - **Cluster Type**: Select the column indicating urban/rural classification
   - **Latitude**: Select the latitude column (decimal degrees)
   - **Longitude**: Select the longitude column (decimal degrees)
   - **Admin Boundaries**: Select the column with administrative unit IDs

4. **Load Centroids**
   - Click the `Load Centroids` button
   - The plugin will create a point layer with your centroids

5. **Review Results**
   - Check the QGIS Layers panel for the new centroids layer
   - Verify points appear in correct locations on the map

#### Expected Output
- A new layer: `[basename]_centroids`
- Points colored by cluster type
- Attribute table with all original fields

---

### Tutorial 2: Loading Centroids from Shapefile

If you already have processed centroids as a shapefile:

1. **Open Tab 1: Centroids Layer**

2. **Select Shapefile**
   - Click `Browse` next to "Centroids Layer"
   - Select your SHP file

3. **Map Fields**
   - **Cluster Number**: Select cluster ID field
   - **Cluster Type**: Select type field
   - **Admin Boundaries**: Select admin field

4. **Load Centroids**
   - Click `Load Centroids`
   - The plugin will import the shapefile

---

### Tutorial 3: Processing Covariates

Extract geospatial data for each cluster location.

#### Prerequisites
- Loaded centroids (from Tutorial 1 or 2)
- A CSV file listing covariate layers
- Raster or vector files for each covariate

#### Covariate CSV Format

Create a CSV with these columns:

```csv
filename,fileformat,sumstat,columnname,nodata
elevation.tif,raster,mean,elevation_mean,-9999
landcover.tif,raster,majority,landcover_type,-9999
population.tif,raster,sum,population_total,
```

**Column Descriptions:**
- `filename`: Name of the raster/vector file
- `fileformat`: Either "raster" or "vector"
- `sumstat`: Statistics to calculate (mean, sum, majority, min, max)
- `columnname`: Name for the output column
- `nodata`: Value to treat as no data (optional)

#### Steps

1. **Open Tab 2: Covariates**

2. **Select Reference Layer**
   - Choose the centroids layer created in previous steps
   - Select the cluster ID field

3. **Load Covariate List**
   - Click `Browse` next to "Covariates Input File"
   - Select your covariate CSV file

4. **Map CSV Fields**
   - Map the CSV columns to the required fields
   - Ensure all mappings are correct

5. **Process Covariates**
   - Click `Process Covariates`
   - Processing time depends on number of layers and cluster count

6. **Review Output**
   - Find the output CSV: `[basename]_output_covariates.csv`
   - Each row represents one cluster
   - Columns include all requested covariate statistics

---

## Input/Output Formats

### Input Formats

#### CSV File (Centroids)
```csv
cluster_id,latitude,longitude,type,admin1
001,15.3456,32.5678,urban,Region1
002,14.2345,31.4567,rural,Region1
```

**Requirements:**
- UTF-8 encoding recommended
- Decimal degrees for coordinates
- Unique cluster IDs
- No missing values in required fields

#### Shapefile (Centroids)
- Point geometry
- Projected or geographic coordinate system
- Attribute table with cluster ID, type, and admin fields

#### Covariate List CSV
```csv
filename,fileformat,sumstat,columnname,nodata
layer1.tif,raster,mean,var1_mean,-9999
```

### Output Formats

#### Centroids Layer
- **Format**: Shapefile
- **Location**: `[output_dir]/[basename]_centroids.shp`
- **Geometry**: Point
- **Attributes**: All original fields plus any calculated fields

#### Covariates CSV
- **Format**: CSV
- **Location**: `[output_dir]/[basename]_output_covariates.csv`
- **Structure**: One row per cluster, columns for each covariate

**Example:**
```csv
fid,cluster,elevation_mean,landcover_type,population_total
1,001,450.5,2,15000
2,002,320.8,1,5000
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: "Plugin not appearing in toolbar"

**Solution:**
1. Go to `Plugins` → `Manage and Install Plugins`
2. Click `Installed` tab
3. Find "MICS GIS PLUGIN"
4. Ensure checkbox is checked
5. Restart QGIS if necessary

#### Issue: "Cannot load CSV file"

**Possible Causes:**
- File encoding issue (use UTF-8)
- Incorrect path or file permissions
- CSV has incorrect format

**Solution:**
1. Open CSV in a text editor to verify format
2. Ensure no special characters in file path
3. Check that required columns exist
4. Verify UTF-8 encoding

#### Issue: "Fields not showing in dropdown"

**Solution:**
1. Verify input file is loaded correctly
2. Check that file format is recognized (CSV or SHP)
3. Reload the file
4. Check QGIS log panel for errors

#### Issue: "Covariate processing fails"

**Possible Causes:**
- Raster files not found
- Coordinate system mismatch
- Invalid nodata values

**Solution:**
1. Ensure all raster files are in the same directory as the CSV
2. Verify coordinate systems match between centroids and rasters
3. Check nodata values are correct
4. Review QGIS log messages for specific errors

#### Issue: "Output files not created"

**Solution:**
1. Verify output directory exists and is writable
2. Check disk space
3. Ensure basename doesn't contain special characters
4. Review QGIS log panel for permission errors

### Getting Help

If you encounter issues not covered here:

1. **Check the QGIS Log Panel**
   - View → Panels → Log Messages
   - Look for error messages from "MICS GIS PLUGIN"

2. **Review Configuration**
   - Verify all file paths are correct
   - Check field mappings
   - Ensure data formats match expectations

3. **Report Issues**
   - GitHub Issues: [Repository URL]
   - Include error messages from log panel
   - Attach sample data if possible (anonymized)

---

## FAQ

### General Questions

**Q: What is the purpose of displacement?**

A: Displacement protects respondent privacy by shifting GPS coordinates. The plugin applies controlled displacement that maintains spatial patterns while preventing identification of specific households.

**Q: Can I process multiple surveys at once?**

A: Currently, the plugin processes one survey at a time. However, you can save configurations and reload them for batch processing.

**Q: What coordinate systems are supported?**

A: The plugin works with any coordinate system supported by QGIS. It automatically handles transformations between different CRS.

### Technical Questions

**Q: Do I need Python programming knowledge?**

A: No. The plugin provides a graphical interface. Python knowledge is only needed if you want to modify the plugin code.

**Q: How much memory do I need?**

A: This depends on dataset size. For typical MICS surveys (100-500 clusters), 4-8 GB RAM is sufficient. Large covariate rasters may require more.

**Q: Can I use this plugin for non-MICS data?**

A: Yes! While designed for MICS, the plugin works with any point-based survey data that needs geocoding and covariate extraction.

**Q: Are there limits on file sizes?**

A: File size limits are determined by QGIS and your system resources, not the plugin itself. Very large rasters (>10 GB) may process slowly.

### Data Questions

**Q: What if my CSV has different column names?**

A: The plugin uses field mapping dropdowns. You can map any column names to the required fields.

**Q: Can I use geographic coordinates (lat/lon)?**

A: Yes, the plugin accepts both geographic (EPSG:4326) and projected coordinate systems.

**Q: What raster formats are supported for covariates?**

A: Any format supported by GDAL/QGIS: GeoTIFF (.tif), HDF, NetCDF, etc.

---

## Next Steps

After completing these tutorials, you should be able to:
- ✅ Install and activate the plugin
- ✅ Load centroids from CSV or shapefile
- ✅ Configure and save project settings
- ✅ Process geospatial covariates
- ✅ Troubleshoot common issues

### Additional Resources

- **Developer Documentation**: See [README.md](README.md) for technical details
- **Release Notes**: See [release-notes.md](release-notes.md) for version history
- **Code Repository**: [GitHub Repository URL]

### Support

For technical support:
- Email: ngashi@unicef.org
- GitHub Issues: [Repository URL]/issues

---

**Authors**: Jan Burdziej (UNICEF), Nazim Gashi (UNICEF), Etienne Delclaux (CartONG)  
**Document Version**: 1.0  
**Last Updated**: October 2025  
**Plugin Version**: 1.3.0
