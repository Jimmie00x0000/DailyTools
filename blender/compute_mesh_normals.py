import bpy
import os

# run 'blender --background --python compute_mesh_normals.py' in command
if __name__ == '__main__':
    # remove the default obj Cube,
    cube_obj = bpy.data.meshes['Cube']
    bpy.data.meshes.remove(cube_obj)

    # visit all plys
    dir_path = './recon'
    for dir_path, dir_names, files in os.walk(dir_path):
        for file_ in files:
            file_path = dir_path + '/' + file_
            if not file_path.endswith('.ply'): continue
            if file_path.endswith('_normals.ply'): continue
            print('Importing %s ...' % file_)
            result_set = bpy.ops.import_mesh.ply(filepath=file_path)
            if 'FINISHED' not in result_set:
                print ("failed to import ply, skipping...")
                continue
            #blender_objs = bpy.data.objects
            # print('blender obj len: %d' % len(blender_objs))
            for name, blender_object in bpy.data.objects.items():
                if blender_object.type != 'MESH': continue
                # select object 
                blender_object.select_set(True)
                bpy.ops.object.mode_set(mode='EDIT')
                print('Computing normals of mesh...')
                bpy.ops.mesh.normals_make_consistent(inside=False)
                # merge the normals so that 
                bpy.ops.mesh.merge_normals()
                new_file_path = file_path[:-4] + '_normals.ply'
                bpy.ops.object.mode_set(mode='OBJECT')
                export_result_set = bpy.ops.export_mesh.ply(filepath=new_file_path, use_mesh_modifiers=False, use_uv_coords=False, use_colors=False)
                if 'FINISHED' not in export_result_set:
                    print ("Warning: failed to export ply ...")
                pass
            pass
    # bpy.ops.import_mesh.ply(filepath='')
    pass