# Blender Plugin
to simplify the FBX asset workflow in Blender


- ![Installation](README.md#Installation)
- ![Features](README.md#Features)
  - ![FBX Exporter](README.md#FBX%20Exporter)
  - ![Material Helper](README.md#Material%20Helper)

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

1. Select top level collections to export by enable/disable the ![Render](https://github.com/magic-j/blender_plugin_for_asset_workflow/blob/main/images/blender_icon_render.PNG) icon in the layer tree view.
    - The collection list in FBX Exporter Panel is instantly updated
2. Check for warning message in the top  
    - Fix them, otherwise this can make problems for the later usage of the assets)
    - ![Warnings](https://github.com/magic-j/blender_plugin_for_asset_workflow/blob/main/images/blender_FbxExporter_warnings.PNG)
        - Missing material assigments
        - Missing UV maps
        - Multi instances of same mesh
3. Define Target Directory
    - ![Target Dir](https://github.com/magic-j/blender_plugin_for_asset_workflow/blob/main/images/blender_FbxExporter_targetDir.PNG)
4. Press [**Export**]
    - The collection name will be used as the filename for the fbx.


### Material Helper
Buttons to speed up the material workflow

![MaterialHelper](https://github.com/magic-j/blender_plugin_for_asset_workflow/blob/main/images/blender_MaterialHelper.PNG)

#### Select objects WITHOUT material
All visible mesh objects in the 3D scene gets selected, if they have no material assigned

#### COPY material from selected
Before clicking the button select all the mesh objects in the 3D scene, that should receive a new material.

And additionally, select as last the mesh object the material assigment should be copied from.

(the last selection is visible by a lighter orange outline color)
