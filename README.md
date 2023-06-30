# Blender Plugin
... to simplify the FBX asset workflow.

This plugin has been specially optimized for preparing 3D assets for the Tacton VizStudio.

But this is not a product component. Tacton is not responsible for this plugin.

- [Installation](README.md#installation)
- [Features](README.md#features)
  - [FBX Exporter](README.md#fbx-exporter)
  - [Material Helper](README.md#material-helper)

## Installation
1. Download the latest .py file from github
2. Start Blender
3. Go in the top menu to [Edit] > [Preferences]
4. Select the [Add-Ons] tab
5. Press the [install] button and select the downloaded .py file
6. Enable the plugin by the checkbox in front of the plugin

After the installation is done, you can find the new functionallities in a new tab [**JBR Tools**] in the right side bar of the 3D Viewport.

![JBR Tools](https://github.com/magic-j/blender_plugin_for_asset_workflow/blob/main/images/blender_JBR_Tools.PNG)

Press [N] in 3D Viewport to toggle the right side bar

## Features

### FBX Exporter
Export maked Blender collection as seperate FBX files

The collection name will be used as the filename for the fbx.

Because Blender only allows unique names, the FBX Exporter removes all automatically added numbers (like ".002") for Dockingpoints (**Empty** objects starting with a **"DP_"*) during the export process, to allow the same Dockingpoint name on multiple FBX files.

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


### Material Helper
Buttons to speed up the material workflow

![MaterialHelper](https://github.com/magic-j/blender_plugin_for_asset_workflow/blob/main/images/blender_MaterialHelper.PNG)

#### Select objects WITHOUT material
All visible mesh objects in the 3D scene gets selected, if they have no material assigned

#### COPY material from selected
Before clicking the button select all the mesh objects in the 3D scene, that should receive a new material.

And additionally, select as last the mesh object the material assigment should be copied from.

(the last selection is visible by a lighter orange outline color)

