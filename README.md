# Blender Plugin
... to simplify the FBX asset workflow.

This plugin has been specially optimized for preparing 3D assets for the Tacton VizStudio.

But this is not a product component.
Tacton is not responsible for this plugin.

- [Installation](README.md#installation)
- [Features](README.md#features)
  - [FBX Exporter](README.md#fbx-exporter)
  - [FBX Importer](README.md#fbx-importer)
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

    Similar to the Blender batch exporter, but with some important adjustments.
    - Quick enable/disable the collection for export independant of selections
    - collection name will be used as FBX name
    - Because Blender only allows unique names, the FBX Exporter removes all automatically added numbers (like ".002") for Dockingpoints (**Empty** objects starting with a **"DP_"*) during the export process, to allow the same Dockingpoint name on multiple FBX files.
    - Quickly re-export many assets by a single button click
    - Early quality check of the mesh data

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

---

### FBX Importer
Two different Buttons for importing FBX files

![Warnings](https://github.com/magic-j/blender_plugin_for_asset_workflow/blob/main/images/blender_FbxImporter.PNG)

For each imported FBX a new collection will be created with the filename of the FBX.

In addition, an optimization process runs on the imported nodes:
1. Delete everything that is not a MESH or a EMPTY
2. Apply scale on every node
3. Remove parenting of nodes (flat)
4. Set consistent display mode & scale for EMPTY's
5. After the import is finished "REMOVE material duplicates" is called

#### batch IMPORT FBX
    Select one or more FBX files to import


#### batch IMPORT FOLDER
    Select folder to recursivly import all included FBX files
    The collection name will also contain the relative file path of the FBX

---

### Material Helper
Buttons to speed up the material workflow

![MaterialHelper](https://github.com/magic-j/blender_plugin_for_asset_workflow/blob/main/images/blender_MaterialHelper.PNG)


#### Select objects WITHOUT material
    All visible mesh objects in the 3D scene gets selected, if they have no material assigned

#### COPY material from selected
    Before clicking the button select all the mesh objects in the 3D scene, that should receive a new material.
    
    And additionally, select as last the mesh object the material assigment should be copied from.
    
    (the last selection is visible by a lighter orange outline color)

#### SEPARATE Multi-Mat meshes
    Before clicking the button select all the mesh objects in the 3D scene, that should be updated.
    (Only works in Object mode.)
    
    All selected mesh objects with Multi-Materials are getting separated into sub-mesh objects with only one material assignment
    
    The names of the new mesh objects contain the respective material name

#### REMOVE material duplicates
    all  materials in the curent blend file are validated
    if a material ends with a number (like .002) and another material with the same base name exists:
    - the material is deleted
    - all meshes with the material assigned are getting updated with the base material
