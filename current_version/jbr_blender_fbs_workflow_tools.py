bl_info = {
    "name": "JBR Tools",
    "blender": (3, 1, 2),
    "category": "Object",
    "author": "Jonas Brügner",
    "location": "3D Viewport -> sidebar right [N]",
    "description": "nice tools for daily work ..."
}

import os
import bpy
import re
from bpy_extras.io_utils import ImportHelper
import textwrap


###############################################################################################
#  3D Viewport Menu
###############################################################################################

#class JbrMenu(bpy.types.Menu):
#    """Scripted operations by JBR"""
#    bl_idname = 'object.jbr_menu'
#    bl_label = 'JBR Tools'
#    bl_description = "Scripted operations by JBR"
#    def draw(self, context):
#        layout = self.layout                
#        #layout.operator(ObjectMoveX.bl_idname)


###############################################################################################
#  FBX Exporter
###############################################################################################

class FolderSelect(bpy.types.PropertyGroup):
    path : bpy.props.StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')
        
        

#class Button_ExportAllCollectionsAsFbx(bpy.types.Operator, ImportHelper):
class Button_ExportAllCollectionsAsFbx(bpy.types.Operator):
    bl_idname = "object.export_fbx_all_collections"
    bl_label = "Export FBX"
    bl_description = "Export all collections as FBX"
    bl_options = {'PRESET', 'REGISTER'}
    
    def ShowMessageBox(self, message = "", title = "Message Box", icon = 'INFO'):
        
        def draw(self, context):
            self.layout.active_default = True
            lines = message.split("\n")
            for line in lines:
                self.layout.label(text=line)

        bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
    
    def fixDockingPointNamesInCollection(self, collection):
        # Check all dockingpoints to remove numeration suffixes
        for obj in collection.all_objects:
            if obj.type == "EMPTY" and obj.name.startswith('DP_'):   # only Dockingpoints                    
                if re.match(".*\\.[0-9]{3}$", obj.name):   # DP name has numeration suffix
                    baseName = obj.name[:-4]                        
                    if bpy.data.objects.get(baseName):   # set name of other DP without numeration suffix to old name, if exists 
                        bpy.data.objects[baseName].name = obj.name
                    print("fix DP '" + obj.name + "' to '" + baseName + "'")                        
                    obj.name = baseName   # remove numeration suffix
    
    def exportFBX(self, fbxPath):
        # Export all mesh+empty of collection to fbx :
        bpy.ops.export_scene.fbx(
            filepath=fbxPath,
            use_active_collection=True,
            object_types={'EMPTY', 'MESH'},
            bake_anim=False,
            bake_anim_use_all_bones=False
        );
    
    def execute(self, context):
        scene = context.scene
                
        filepath = context.scene.folder_select_prop.path
        if (filepath == ""):
            self.ShowMessageBox("Please define a export directory !", " Export failed!", "ERROR")
            return {'CANCELLED'}
        
        filepath = bpy.path.abspath(filepath) # fix relative path
        filepath = os.path.normpath(filepath) # remove all /../ 
        
        if (not os.path.exists(filepath)):
            self.ShowMessageBox("Please define a valid export directory !", " Export failed!", "ERROR")
            return {'CANCELLED'}
        
        print('Start Export FBX files : ', filepath)
        
        context.scene.folder_select_prop.path = filepath
        fbxNames = []
        for collection in bpy.data.collections:
            if collection.hide_render:
                continue         
            layerCollection = bpy.context.view_layer.layer_collection.children[collection.name]
            context.view_layer.active_layer_collection = layerCollection # Set collection to active            
            self.fixDockingPointNamesInCollection(collection)            
            fbxNames.append(collection.name + ".fbx")
            fbx_path = bpy.path.abspath(filepath + collection.name + ".fbx")
            self.exportFBX(fbxPath=fbx_path);
            
        if (len(fbxNames) == 0):            
            self.ShowMessageBox("Please define the collections to export by enabling their RENDER icon in layer tree view!", " Export failed!", "ERROR")
            return {'CANCELLED'}
            
        message = str(len(fbxNames)) + " collection(s) exported:\n"
        for fbxName in fbxNames:
            message += "\n" + fbxName
        self.ShowMessageBox(message, " Export done", "INFO")
        
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

   
class JbrMenuPanel_FbxExport(bpy.types.Panel):
    bl_idname = 'VIEW_3D_PT_jbr_fbxexporter_panel'
    bl_label = 'FBX Exporter'
    bl_description = "Scripted operations by JonasB."
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "JBR Tools"
    
    def draw_header(self, context):
        layout = self.layout
        #layout.operator("object.select_random", text="R")
    
    def check_error_collection_data(self, collection, grid):
        error = False        
        meshNames = []
        for obj in collection.all_objects:
            if obj.type == "MESH":
                meshName = obj.data.name
                if (meshName in meshNames):
                    self.createErrorEntry(grid, collection.name, "MESH_DATA", "Multiple use of same mesh '" + meshName + "'", not error)
                    error = True
                meshNames.append(meshName)
                uvLayerCount = len(obj.data.uv_layers)                
                if (uvLayerCount == 0):
                    self.createErrorEntry(grid, collection.name, "UV", "No UV layer on mesh '" + meshName + "'", not error)
                    error = True
                matCount = len(obj.data.materials)
                if (matCount == 0 or obj.data.materials[0] is None):
                    self.createErrorEntry(grid, collection.name, "MATERIAL", "No material on mesh '" + meshName + "'", not error)
                    error = True
                        
        return error
    
    def createErrorEntry(self, parent, collectionName, _icon, _text, isFirst):
        if (isFirst):
            cRow = parent.row()
            cRow.alert = True
            cRow.label(text=collectionName,icon="ERROR",translate=False);
            
        row = parent.row()
        row.label(text=_text,icon=_icon,translate=False);
    
    def draw(self, context):
        layout = self.layout        
        
        box = layout.box()
        row = box.row()
        row.label(text="", icon="INFO")
        row.label(text="To export collection enable ", icon="NONE")
        row.label(text="", icon="RESTRICT_RENDER_OFF")
                
        layout.separator(factor=2.0)
        layout.label(text="Export collections [FBX] :")
        error_grid = box.column(align=False, heading='', heading_ctxt='', translate=False)
        
        layout.separator(factor=2.0)
        grid = layout.grid_flow(row_major=True,columns = 0, align=True, even_columns =True, even_rows=True)
        for collection in bpy.data.collections:
            if not collection.hide_render:
                icon = "OUTLINER_COLLECTION"
                if (collection.color_tag != "NONE"):
                    icon = "COLLECTION_" + collection.color_tag
                grid.label(text=collection.name,icon=icon,translate=False);
                self.check_error_collection_data(collection, error_grid)
            
        
        
        col = layout.column(align=True)
        col.prop(context.scene.folder_select_prop, "path", text="")
        
        layout.operator(Button_ExportAllCollectionsAsFbx.bl_idname, icon="EXPORT")


        

###############################################################################################
#  Material Helper
###############################################################################################

class Button_SelectAllObjectsWithoutMaterial(bpy.types.Operator):
    bl_idname = "object.select_objects_without_material"
    bl_label = "Select objects WITHOUT material"

    def execute(self, context):
        scene = context.scene
        
        bpy.ops.object.select_all(action='DESELECT')
        
        visible_objects=[ob for ob in bpy.context.view_layer.objects if ob.visible_get()]
        print('Object count : ', len(visible_objects))       
        for obj in visible_objects:
            print('Object : ', obj.name)          
            
            if obj.type == "MESH":
                meshName = obj.data.name
                matCount = len(obj.data.materials)
                if (matCount == 0 or obj.data.materials[0] is None):
                    obj.select_set(True)
        
        return {'FINISHED'}

class Button_CopyMaterialFromSelected(bpy.types.Operator):
    bl_idname = "object.copy_material_from_selected"
    bl_label = "COPY material from selected"

    def execute(self, context):
        bpy.ops.object.make_links_data(type="MATERIAL")
        return {'FINISHED'}
    
class JbrMenuPanel_MaterialHelper(bpy.types.Panel):
    bl_idname = 'VIEW_3D_PT_jbr_materialhelper_panel'
    bl_label = 'Material Helper'
    bl_description = "Scripted operations by JonasB."
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "JBR Tools"
    
    def draw_header(self, context):
        layout = self.layout
        
    def draw(self, context):
        layout = self.layout
        
        layout.operator(Button_SelectAllObjectsWithoutMaterial.bl_idname,  icon="NODE_MATERIAL")        
        
        layout.operator(Button_CopyMaterialFromSelected.bl_idname,  icon="COPYDOWN")



###############################################################################################
#  INSTALL
###############################################################################################

def menu_func_build(self, context):    
    self.layout.menu(JbrMenuPanel_FbxExport.bl_idname)
    self.layout.menu(JbrMenuPanel_MaterialHelper.bl_idname)

def register():    
    bpy.utils.register_class(FolderSelect)
    bpy.utils.register_class(Button_ExportAllCollectionsAsFbx)
    bpy.utils.register_class(Button_SelectAllObjectsWithoutMaterial)
    bpy.utils.register_class(Button_CopyMaterialFromSelected)
    bpy.utils.register_class(JbrMenuPanel_MaterialHelper)
    bpy.utils.register_class(JbrMenuPanel_FbxExport)
    
    bpy.types.Scene.folder_select_prop = bpy.props.PointerProperty(type=FolderSelect)
    
    bpy.types.VIEW3D_MT_object.append(menu_func_build)

def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func_build)
    
    del bpy.types.Scene.folder_select_prop
    
    bpy.utils.unregister_class(FolderSelect)
    bpy.utils.unregister_class(Button_ExportAllCollectionsAsFbx)
    bpy.utils.unregister_class(Button_SelectAllObjectsWithoutMaterial)
    bpy.utils.unregister_class(Button_CopyMaterialFromSelected)
    bpy.utils.unregister_class(JbrMenuPanel_MaterialHelper)
    bpy.utils.unregister_class(JbrMenuPanel_FbxExport)
    

# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()