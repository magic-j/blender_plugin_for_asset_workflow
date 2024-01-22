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


from bpy.types import bpy_prop_collection

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
            fbx_path = bpy.path.abspath(filepath + "\\" + collection.name + ".fbx")
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
#  FBX Importer
###############################################################################################

class Button_ImportFbxAsCollections(bpy.types.Operator, ImportHelper):
    bl_idname = "object.import_fbx_as_collections"
    bl_label = "batch IMPORT FBX"
    bl_description = "Import all selected FBX and create a new collection for each"

    filter_glob: bpy.props.StringProperty(
        default='*.fbx',
        options={'HIDDEN'}
    )

    directory: bpy.props.StringProperty(
        options={'HIDDEN'}
    )

    files: bpy.props.CollectionProperty(
        #name='File paths',
        type=bpy.types.OperatorFileListElement,
        options={'HIDDEN', 'SKIP_SAVE'}
    )

    def importFbxAsCollection(self, fbxPath, collectionName):
        # Import all mesh+empty of collection to fbx :
        
        bpy.ops.object.select_all(action='DESELECT')
        
        bpy.ops.import_scene.fbx(
            use_anim = False,
            # global_scale = 1.0,
            # bake_space_transform = False,
            filepath = fbxPath
        );
        imported_objecs = bpy.context.selected_objects

        collection = bpy.context.blend_data.collections.new(name=collectionName)
        bpy.context.collection.children.link(collection)


        for obj in imported_objecs:            
        
            for coll in obj.users_collection:
                # Unlink the object
                coll.objects.unlink(obj)
                
            collection.objects.link(obj)       
            
            if not obj.type == 'EMPTY' and not obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)     
                bpy.ops.object.delete()
                continue
            
            if (not obj.parent == None):
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)                
                bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            
            if obj.type == 'EMPTY':                
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)                
                bpy.ops.object.transform_apply(scale=True,   location=False, rotation=False, properties=False, isolate_users=False)
                
                if obj.name.startswith('DP_'):
                    obj.empty_display_type = 'ARROWS'
                    obj.empty_display_size = 0.1
                else:                    
                    obj.empty_display_type = 'SPHERE'
                    obj.empty_display_size = 0.02
        
    
    def execute(self, context):
        print('\nButton_ImportFbxAsCollections')

        
        #if not os.path.isdir(import_dir):
        #    self.report({'WARNING'}, "Please select a directory")
        #    return {'CANCELLED'}

        bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection

        file_count = len(self.files)
        file_index = 0
        bpy.context.window_manager.progress_begin(0, file_count)

        for fileElement in self.files:
            filename, extension = os.path.splitext(fileElement.name)
            fbxPath = self.directory + fileElement.name
            print(fbxPath)            
            if not os.path.isfile(fbxPath):
                self.report({'WARNING'}, "Please select a file")
                return {'CANCELLED'}
            self.importFbxAsCollection(fbxPath, filename)
            file_index += 1            
            bpy.context.window_manager.progress_update(file_index)

        bpy.ops.object.select_all(action='DESELECT')

        bpy.ops.object.remove_material_duplicates()

        bpy.context.window_manager.progress_end()

        return {'FINISHED'}


class Button_ImportFolderRecursiveAsCollections(bpy.types.Operator, ImportHelper):
    bl_idname = "object.import_folder_recursive_as_collections"
    bl_label = "batch IMPORT FOLDER"
    bl_description = "Import all FBX recursively from a selected directory and create a new collection for each"

    use_filter_folder = True

    def importFbxAsCollection(self, fbxPath, collectionName):
        # Import all mesh+empty of collection to fbx :
        
        bpy.ops.object.select_all(action='DESELECT')
        
        bpy.ops.import_scene.fbx(
            filepath = fbxPath
        );
        imported_objecs = bpy.context.selected_objects

        collection = bpy.context.blend_data.collections.new(name=collectionName)
        bpy.context.collection.children.link(collection)
        

        for obj in imported_objecs:            
        
            for coll in obj.users_collection:
                # Unlink the object
                coll.objects.unlink(obj)
                
            collection.objects.link(obj)
            
            if not obj.type == 'EMPTY' and not obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)     
                bpy.ops.object.delete()
                continue
            
            if (not obj.parent == None):
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)       
                bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            
            if obj.type == 'EMPTY':
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)                
                bpy.ops.object.transform_apply(scale=True,   location=False, rotation=False, properties=False, isolate_users=False)
                
                if obj.name.startswith('DP_'):
                    obj.empty_display_type = 'ARROWS'
                    obj.empty_display_size = 0.1
                else:                    
                    obj.empty_display_type = 'SPHERE'
                    obj.empty_display_size = 0.02

    def importFolder(self, directory, path):
        print("import folder : ", directory)
        files = os.listdir(directory)
        for file in files:
            if not os.path.isdir(directory + file):
                filename, extension = os.path.splitext(file)
                if extension == ".fbx":
                    fbxPath = directory + file
                    print(fbxPath)
                    if not path == "":
                        filename = path + "\\" + filename
                    self.importFbxAsCollection(fbxPath, filename)
            else:
                newPath = file
                if not path == "":
                    newPath = path + "\\" + newPath
                self.importFolder(directory + file + "\\", newPath)

    def execute(self, context):
        print('\nButton_ImportFolderRecursiveAsCollections')
        
        bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection

        import_dir = self.properties.filepath

        if not os.path.isdir(import_dir):
            self.report({'WARNING'}, "Please select a directory")
            return {'CANCELLED'}
            
        self.importFolder(import_dir, "")
        
        #for fileElement in self.files:
        #    filename, extension = os.path.splitext(fileElement.name)
        #    fbxPath = self.directory + fileElement.name
        #    print(fbxPath)
        #    self.importFbxAsCollection(fbxPath, filename)

        context.scene.folder_select_prop.path = import_dir

        bpy.ops.object.select_all(action='DESELECT')

        bpy.ops.object.remove_material_duplicates()

        return {'FINISHED'}

class JbrMenuPanel_FbxImporter(bpy.types.Panel):
    bl_idname = 'VIEW_3D_PT_jbr_fbximporter_panel'
    bl_label = 'FBX Importer'
    bl_description = "Scripted operations by JonasB."
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "JBR Tools"
    
    def draw_header(self, context):
        layout = self.layout
        
    def draw(self, context):
        layout = self.layout
        
        layout.operator(Button_ImportFbxAsCollections.bl_idname,  icon="IMPORT")
        
        layout.operator(Button_ImportFolderRecursiveAsCollections.bl_idname,  icon="IMPORT")

###############################################################################################
#  Material Helper
###############################################################################################

class Button_SelectAllObjectsWithoutMaterial(bpy.types.Operator):
    bl_idname = "object.select_objects_without_material"
    bl_label = "Select meshes WITHOUT material"
    bl_description = "Select all the mesh objects in the scene without a material assignment"

    def execute(self, context):
        print('Button_SelectAllObjectsWithoutMaterial')
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
    bl_label = "COPY material from selected mesh"
    bl_description = "Assigning the first material of the main selection to all the other selected mesh objects"


    def execute(self, context):
        print('Button_CopyMaterialFromSelected')
        bpy.ops.object.make_links_data(type="MATERIAL")
        return {'FINISHED'}
    

class Button_SeparateSelectedMeshesMultiMaterials(bpy.types.Operator):
    bl_idname = "object.separate_meshes_multi_materials"
    bl_label = "SEPARATE Multi-Mat meshes"
    bl_description = "SEPARATE all selected mesh objects with Multi-Materials into sub-mesh objects with only one material assignment"

    def ShowMessageBox(self, message = "", title = "Message Box", icon = 'INFO'):
        
        def draw(self, context):
            self.layout.active_default = True
            lines = message.split("\n")
            for line in lines:
                self.layout.label(text=line)

        bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

    def separateMultiMatMesh(self, obj):
        meshName = obj.data.name
        matCount = len(obj.data.materials)
        print(obj.name, ': separate mesh ', meshName, ' with ', str(matCount), " materials")
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')

        new_mesh_objects = []
        
        for index, mat in enumerate(obj.data.materials):        
            bpy.ops.object.mode_set(mode='EDIT')    
            
            print("slot", str(index), ":", mat.name)
            faceMaterialIndicies = [x.material_index for x in obj.data.polygons]
            if not index in faceMaterialIndicies:
                print("   No faces selected, material " + str(index) + " '" + mat.name + "' not assigned")    
                continue
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.context.object.active_material_index = index
            bpy.ops.object.material_slot_select()
            bpy.ops.mesh.separate(type='SELECTED')
            print(" - sub mesh separated!")
            
            for o in bpy.context.selected_objects:
                if not o == bpy.context.active_object:
                    newName = bpy.context.active_object.name + "_" + mat.name
                    print(" - rename '" + o.name + "' :", newName)
                    o.name = newName
                    new_mesh_objects.append(o)
                    
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            
        bpy.ops.object.mode_set(mode='OBJECT')
                
        for o in new_mesh_objects:
            print("clean up materials of", o.name)
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = o
            o.select_set(True)
            bpy.ops.object.material_slot_remove_unused()

        print("delete ", obj.name)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.delete(use_global=False, confirm=False)

    def execute(self, context):
        print('Button_SeparateSelectedMeshesMultiMaterials')
        
        selected_objects = bpy.context.selected_objects
        
        if len(selected_objects) < 1:
            self.ShowMessageBox("Please select one or more mesh objects", " Action failed!", "ERROR")
            return {'CANCELLED'}
        
        if not bpy.context.object.mode == 'OBJECT':
            self.ShowMessageBox("Please switch to object mode", " Action failed!", "ERROR")
            return {'CANCELLED'}
        
        bpy.ops.object.select_all(action='DESELECT')
        for obj in selected_objects:
            if not obj.type == "MESH":
                continue

            if len(obj.data.materials) > 1:
                self.separateMultiMatMesh(obj)    
        
        return {'FINISHED'}
        
class Button_RemoveMaterialDuplicates(bpy.types.Operator):
    bl_idname = "object.remove_material_duplicates"
    bl_label = "REMOVE material duplicates"
    bl_description = "REMOVE all materials that are duplicates and fixes the assigment of all users"

    def ShowMessageBox(self, message = "", title = "Message Box", icon = 'INFO'):
        def draw(self, context):
            self.layout.active_default = True
            lines = message.split("\n")
            for line in lines:
                self.layout.label(text=line)

        bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

    def search(self, ID):
        def users(col):
            ret = tuple(repr(o) for o in col if o.user_of_id(ID))
            return ret if ret else None
        return filter(
            None,
            (
                users(getattr(bpy.data, p)) 
                for p in  dir(bpy.data) 
                if isinstance(
                    getattr(bpy.data, p, None), 
                    bpy_prop_collection
                )                
            )
        )

    def execute(self, context):
        print('Button_RemoveMaterialDuplicates')
                
        allMaterials = bpy.data.materials
        
        for mat in allMaterials:
            if mat.is_grease_pencil:
                continue
            if not re.match(".*\\.[0-9]{3}$", mat.name):
                continue
            baseMatName = mat.name[:-4]
            if not baseMatName in allMaterials:
                print("No base material found for :", mat.name)
                continue
                
            print(mat.name, ":", str(mat.users))
            print("new name:", baseMatName)
            
            mat.user_remap(allMaterials[baseMatName])
            bpy.data.materials.remove(mat)
        
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
        
        layout.operator(Button_SeparateSelectedMeshesMultiMaterials.bl_idname,  icon="MATERIAL_DATA")    

        layout.operator(Button_RemoveMaterialDuplicates.bl_idname,  icon="GHOST_DISABLED") 



###############################################################################################
#  INSTALL
###############################################################################################

def menu_func_build(self, context):    
    self.layout.menu(JbrMenuPanel_MaterialHelper.bl_idname)
    self.layout.menu(JbrMenuPanel_FbxImporter.bl_idname)
    self.layout.menu(JbrMenuPanel_FbxExport.bl_idname)

def register():    
    bpy.utils.register_class(FolderSelect)
    bpy.utils.register_class(Button_ExportAllCollectionsAsFbx)
    bpy.utils.register_class(Button_ImportFbxAsCollections)
    bpy.utils.register_class(Button_ImportFolderRecursiveAsCollections)
    bpy.utils.register_class(Button_SelectAllObjectsWithoutMaterial)
    bpy.utils.register_class(Button_CopyMaterialFromSelected)
    bpy.utils.register_class(Button_SeparateSelectedMeshesMultiMaterials)
    bpy.utils.register_class(Button_RemoveMaterialDuplicates)
    bpy.utils.register_class(JbrMenuPanel_MaterialHelper)
    bpy.utils.register_class(JbrMenuPanel_FbxImporter)
    bpy.utils.register_class(JbrMenuPanel_FbxExport)
    
    bpy.types.Scene.folder_select_prop = bpy.props.PointerProperty(type=FolderSelect)
    
    bpy.types.VIEW3D_MT_object.append(menu_func_build)

def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func_build)
    
    del bpy.types.Scene.folder_select_prop
    
    bpy.utils.unregister_class(FolderSelect)
    bpy.utils.unregister_class(Button_ExportAllCollectionsAsFbx)
    bpy.utils.unregister_class(Button_ImportFbxAsCollections)
    bpy.utils.unregister_class(Button_ImportFolderRecursiveAsCollections)
    bpy.utils.unregister_class(Button_SelectAllObjectsWithoutMaterial)
    bpy.utils.unregister_class(Button_CopyMaterialFromSelected)
    bpy.utils.unregister_class(Button_SeparateSelectedMeshesMultiMaterials)
    bpy.utils.unregister_class(Button_RemoveMaterialDuplicates)
    bpy.utils.unregister_class(JbrMenuPanel_MaterialHelper)
    bpy.utils.unregister_class(JbrMenuPanel_FbxImporter)
    bpy.utils.unregister_class(JbrMenuPanel_FbxExport)
    

# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()