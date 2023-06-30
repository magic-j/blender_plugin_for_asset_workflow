# Blender Plugin
to simplify the FBX asset workflow in Blender


- [Installation]
- [Features]
  - [FBX Exporter]
  - [Material Helper]

## Installation
1. Download the latest .py file from github
2. Start Blender
3. Go in the top menu to [Edit] > [Preferences]
4. Select the [Add-Ons] tab
5. Press the [install] button and select the downloaded .py file
6. Enable the plugin by the checkbox in front of the plugin

## Features

### FBX Exporter
Export maked Blender collection as seperate FBX files

1. Select collection to export by enable/disable the [Render] icon in the layer tree view.
2. Check for warning message in the top and fix them.
(Otherwise this can make problems for the later usage of the assets)
  - Missing material assigments
  - Missing UV maps
  - Multi instances of same mesh
3. Define Target Directory
4. Press [**Export**]

The collection name will be used as the filename for the fbx.


### Material Helper
Buttons to speed up the material workflow

[**Select objects WITHOUT material**]

[**COPY mateiral from selected**]